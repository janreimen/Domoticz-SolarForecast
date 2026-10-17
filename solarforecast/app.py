"""Domoticz-independent orchestration for the Solar Forecast plugin."""
import json
import os
import time
from datetime import datetime
from pathlib import Path

from . import __version__
from .api import fetch_forecast
from .config import load_env_file, parse_config
from .devices import (
    REMAINING_TODAY_UNIT, TOMORROW_UNIT, STATUS_UNIT, NEXT_HOUR_UNIT,
    FORECAST_ENERGY_COUNTER_UNIT, REMAINING_TODAY_DETAIL_UNIT, ensure_devices, update_unit,
)
from .forecast import parse_forecast


class SolarForecastApp:
    HEARTBEAT_SECONDS = 10

    def __init__(self, domoticz, devices_provider, settings_provider, plugin_dir,
                 fetcher=None, clock=None, now_provider=None):
        self.domoticz = domoticz
        self.devices_provider = devices_provider
        self.settings_provider = settings_provider
        self.plugin_dir = Path(plugin_dir)
        self.fetcher = fetcher or fetch_forecast
        self.clock = clock or time.time
        self.now_provider = now_provider or datetime.now
        self.counter_state_path = self.plugin_dir / ".solarforecast_counter.json"
        self.config = None
        self.heartbeat_count = 0
        self.last_success = None
        self.log_level = "INFO"
        self.counter_state = {
            "total_wh": 0,
            "last_accounted_hour": None,
            "pending_hour": None,
            "pending_wh": None,
        }
        self._load_counter_state()

    def log(self, level, message):
        levels = {"ERROR": 0, "WARNING": 1, "INFO": 2, "DEBUG": 3, "TRACE": 4}
        if levels.get(level, 2) > levels.get(self.log_level, 2):
            return
        safe = str(message)
        if self.config and self.config.get("API_KEY"):
            safe = safe.replace(self.config["API_KEY"], "<redacted>")
        if level == "ERROR":
            self.domoticz.Error(safe)
        elif level in ("DEBUG", "TRACE"):
            self.domoticz.Debug(safe)
        else:
            self.domoticz.Log(safe)

    def _load_counter_state(self):
        """Restore lifetime forecast total and pending hour across restarts."""
        try:
            with self.counter_state_path.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            self.counter_state.update({key: loaded[key] for key in self.counter_state
                                       if key in loaded})
            self.counter_state["total_wh"] = max(0, int(self.counter_state["total_wh"]))
        except FileNotFoundError:
            pass
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            # Keep the counter alive with safe defaults if the state file is damaged.
            self.domoticz.Error("Could not read forecast counter state: {}".format(exc))

    def _save_counter_state(self):
        """Write state atomically to avoid a partial file on power loss."""
        temporary = self.counter_state_path.with_suffix(".json.tmp")
        try:
            self.plugin_dir.mkdir(parents=True, exist_ok=True)
            with temporary.open("w", encoding="utf-8") as handle:
                json.dump(self.counter_state, handle, sort_keys=True)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(str(temporary), str(self.counter_state_path))
        except OSError as exc:
            self.log("ERROR", "Could not persist forecast counter state: {}".format(exc))
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass

    @staticmethod
    def _hour_key(value):
        if isinstance(value, datetime):
            return value.replace(minute=0, second=0, microsecond=0).isoformat(timespec="seconds")
        return str(value)

    def _account_due_forecast(self, now):
        """Add a pending forecast once its forecast hour has begun."""
        pending_hour = self.counter_state.get("pending_hour")
        pending_wh = self.counter_state.get("pending_wh")
        if not pending_hour or pending_wh is None:
            return False
        try:
            due = datetime.fromisoformat(pending_hour) <= now
        except (TypeError, ValueError):
            self.log("WARNING", "Invalid pending forecast hour {}; ignoring it".format(pending_hour))
            self.counter_state["pending_hour"] = None
            self.counter_state["pending_wh"] = None
            return False
        if not due or pending_hour == self.counter_state.get("last_accounted_hour"):
            return False
        increment_wh = max(0, int(round(float(pending_wh))))
        self.counter_state["total_wh"] = int(self.counter_state["total_wh"]) + increment_wh
        self.counter_state["last_accounted_hour"] = pending_hour
        self.log("INFO", "Forecast counter +{:.3f} kWh for hour {}; total {:.3f} kWh".format(
            increment_wh / 1000.0, pending_hour, self.counter_state["total_wh"] / 1000.0))
        return True

    def on_start(self):
        try:
            self.config = parse_config(
                load_env_file(self.plugin_dir / ".env"), self.settings_provider())
            self.log_level = self.config["LOG_LEVEL"]
            debug_level = 2 if self.log_level in ("DEBUG", "TRACE") else 1 if self.log_level == "INFO" else 0
            self.domoticz.Debugging(debug_level)
            self.heartbeat_count = max(1, int(
                self.config["POLL_INTERVAL_MINUTES"] * 60 / self.HEARTBEAT_SECONDS))
            ensure_devices(self.domoticz, self.devices_provider())
            self.log("INFO", "Solar Forecast v{} started; poll interval={} min.".format(
                __version__, self.config["POLL_INTERVAL_MINUTES"]))
            self.poll()
        except Exception as exc:
            self.log("ERROR", "Startup failed: {}".format(exc))

    def on_stop(self):
        self.log("INFO", "Solar Forecast stopped")

    def on_heartbeat(self):
        if not self.config:
            return
        self.heartbeat_count -= 1
        if self.heartbeat_count <= 0:
            self.heartbeat_count = max(1, int(
                self.config["POLL_INTERVAL_MINUTES"] * 60 / self.HEARTBEAT_SECONDS))
            self.poll()

    def on_command(self, unit, command, level, color):
        self.log("DEBUG", "Ignoring command for read-only forecast unit {}".format(unit))

    def poll(self):
        try:
            now = self.now_provider()
            forecast = parse_forecast(self.fetcher(self.config), now=now)
            remaining_today_wh = max(0, int(forecast["remaining_today_wh"]))
            tomorrow_wh = forecast["tomorrow_wh"]
            # Unit 1 spans now through the end of tomorrow; unit 6 exposes
            # the today-only component derived from that horizon.
            remaining_until_tomorrow_wh = (remaining_today_wh + int(tomorrow_wh)
                                           if tomorrow_wh is not None else remaining_today_wh)
            remaining_until_tomorrow_kwh = remaining_until_tomorrow_wh / 1000.0
            tomorrow_kwh = int(tomorrow_wh) / 1000.0 if tomorrow_wh is not None else 0.0
            today_kwh = max(0, remaining_until_tomorrow_wh - int(tomorrow_wh or 0)) / 1000.0
            next_hour_wh = max(0, int(forecast["next_hour_wh"]))
            next_hour_kwh = next_hour_wh / 1000.0
            devices = self.devices_provider()
            update_unit(self.domoticz, devices, REMAINING_TODAY_UNIT,
                        "{:.3f}".format(remaining_until_tomorrow_kwh), self.log)
            update_unit(self.domoticz, devices, REMAINING_TODAY_DETAIL_UNIT,
                        "{:.3f}".format(today_kwh), self.log)
            update_unit(self.domoticz, devices, TOMORROW_UNIT,
                        "{:.3f}".format(tomorrow_kwh), self.log)
            update_unit(self.domoticz, devices, NEXT_HOUR_UNIT,
                        "{:.3f}".format(next_hour_kwh), self.log)

            # First account the previous sample once its target hour has started.
            changed = self._account_due_forecast(now)
            target_hour = self._hour_key(forecast["next_hour_start"])
            last_accounted = self.counter_state.get("last_accounted_hour")
            if target_hour != last_accounted:
                self.counter_state["pending_hour"] = target_hour
                self.counter_state["pending_wh"] = next_hour_wh
            # At an exact hour boundary the forecast can refer to the current hour;
            # count it now. Otherwise it stays pending until that hour begins.
            changed = self._account_due_forecast(now) or changed
            self._save_counter_state()

            total_wh = int(self.counter_state["total_wh"])
            # Native Domoticz generated-energy meter format: power in W; cumulative
            # generated energy in Wh. Switchtype=4 marks this as energy return, not usage.
            # For a one-hour forecast block, Wh is numerically equal to average W.
            update_unit(self.domoticz, devices, FORECAST_ENERGY_COUNTER_UNIT,
                        "{};{}".format(next_hour_wh, total_wh), self.log, force=changed)

            if tomorrow_wh is None:
                status = "PARTIAL - until tomorrow 23:59 {:.3f}; next full hour {:.3f} kWh; tomorrow unavailable".format(
                    remaining_until_tomorrow_kwh, next_hour_kwh)
                self.log("WARNING", "No daily forecast returned for tomorrow ({})".format(forecast["tomorrow"]))
            else:
                status = "OK - next full hour {:.3f}; until tomorrow 23:59 {:.3f}; forecast tomorrow {:.3f}; remaining today {:.3f} kWh".format(
                    next_hour_kwh, remaining_until_tomorrow_kwh, tomorrow_kwh, today_kwh)
                self.log("INFO", "Updated forecast: next full hour {:.3f} kWh; remaining until tomorrow 23:59 {:.3f} kWh; forecast tomorrow {:.3f} kWh; remaining today {:.3f} kWh".format(
                    next_hour_kwh, remaining_until_tomorrow_kwh, tomorrow_kwh, today_kwh))
            update_unit(self.domoticz, devices, STATUS_UNIT, status, self.log)
            self.last_success = self.clock()
        except Exception as exc:
            self.log("ERROR", "Forecast poll failed: {}".format(exc))
            update_unit(self.domoticz, self.devices_provider(), STATUS_UNIT,
                        "ERROR - {}".format(str(exc)[:180]), self.log)
