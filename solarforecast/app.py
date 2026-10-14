"""Domoticz-independent orchestration for the Solar Forecast plugin."""
import time
from pathlib import Path

from . import __version__
from .api import fetch_forecast
from .config import load_env_file, parse_config
from .devices import (
    REMAINING_TODAY_UNIT, TOMORROW_UNIT, STATUS_UNIT, NEXT_HOUR_UNIT,
    ensure_devices, update_unit,
)
from .forecast import parse_forecast


class SolarForecastApp:
    HEARTBEAT_SECONDS = 10

    def __init__(self, domoticz, devices_provider, settings_provider, plugin_dir,
                 fetcher=None, clock=None):
        self.domoticz = domoticz
        self.devices_provider = devices_provider
        self.settings_provider = settings_provider
        self.plugin_dir = Path(plugin_dir)
        self.fetcher = fetcher or fetch_forecast
        self.clock = clock or time.time
        self.config = None
        self.heartbeat_count = 0
        self.last_success = None
        self.log_level = "INFO"

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
            forecast = parse_forecast(self.fetcher(self.config))
            today_kwh = forecast["remaining_today_wh"] / 1000.0
            tomorrow_wh = forecast["tomorrow_wh"]
            tomorrow_kwh = tomorrow_wh / 1000.0 if tomorrow_wh is not None else 0.0
            next_hour_kwh = forecast["next_hour_wh"] / 1000.0
            devices = self.devices_provider()
            update_unit(self.domoticz, devices, REMAINING_TODAY_UNIT,
                        "{:.3f}".format(today_kwh), self.log)
            update_unit(self.domoticz, devices, TOMORROW_UNIT,
                        "{:.3f}".format(tomorrow_kwh), self.log)
            update_unit(self.domoticz, devices, NEXT_HOUR_UNIT,
                        "{:.3f}".format(next_hour_kwh), self.log)
            if tomorrow_wh is None:
                status = "PARTIAL - today {:.3f}; next hour {:.3f} kWh; tomorrow unavailable".format(
                    today_kwh, next_hour_kwh)
                self.log("WARNING", "No daily forecast returned for tomorrow ({})".format(forecast["tomorrow"]))
            else:
                status = "OK - today {:.3f}; next hour {:.3f}; tomorrow {:.3f} kWh".format(
                    today_kwh, next_hour_kwh, tomorrow_kwh)
                self.log("INFO", "Updated forecast: today remaining {:.3f} kWh; next full hour {:.3f} kWh; tomorrow {:.3f} kWh".format(
                    today_kwh, next_hour_kwh, tomorrow_kwh))
            update_unit(self.domoticz, devices, STATUS_UNIT, status, self.log)
            self.last_success = self.clock()
        except Exception as exc:
            self.log("ERROR", "Forecast poll failed: {}".format(exc))
            update_unit(self.domoticz, self.devices_provider(), STATUS_UNIT,
                        "ERROR - {}".format(str(exc)[:180]), self.log)
