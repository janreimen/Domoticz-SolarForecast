import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from solarforecast.app import SolarForecastApp
from solarforecast.devices import FORECAST_ENERGY_COUNTER_UNIT, REMAINING_TODAY_DETAIL_UNIT


class FakeDevice:
    def __init__(self, value=""):
        self.nValue = 0
        self.sValue = value
        self.calls = []
    def Update(self, nValue, sValue):
        self.calls.append((nValue, sValue))
        self.nValue, self.sValue = nValue, sValue


class FakeDomoticz:
    def Log(self, message): pass
    def Error(self, message): pass
    def Debug(self, message): pass
    def Debugging(self, level): pass


class ForecastCounterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.plugin_dir = Path(self.temp.name)
        self.now = datetime(2026, 10, 15, 12, 30)
        self.devices = {unit: FakeDevice() for unit in (1, 2, 3, 4, FORECAST_ENERGY_COUNTER_UNIT, REMAINING_TODAY_DETAIL_UNIT)}
        self.wh_by_hour = {13: 1300, 14: 1400, 15: 1500}

        def fetcher(config):
            periods = {
                "2026-10-15 12:00:00": 1200,
                "2026-10-15 13:00:00": self.wh_by_hour[13],
                "2026-10-15 14:00:00": self.wh_by_hour[14],
                "2026-10-15 15:00:00": self.wh_by_hour[15],
                "2026-10-15 16:00:00": 1600,
            }
            return {"message": {"type": "success", "text": "ok"}, "result": {
                "watt_hours_period": periods,
                "watt_hours_day": {"2026-10-16 00:00:00": 5500},
            }}
        self.fetcher = fetcher

    def tearDown(self):
        self.temp.cleanup()

    def make_app(self):
        app = SolarForecastApp(FakeDomoticz(), lambda: self.devices,
                               lambda: {"Location": "49.71;6.25;0"},
                               self.plugin_dir, fetcher=self.fetcher,
                               clock=lambda: 1, now_provider=lambda: self.now)
        app.config = {"LOG_LEVEL": "ERROR", "API_KEY": "", "POLL_INTERVAL_MINUTES": 10}
        return app

    def test_accumulates_forecast_once_when_hour_begins(self):
        app = self.make_app()
        app.poll()  # 12:30: saves the forecast for 13:00, but does not count it yet.
        self.assertEqual(app.counter_state["total_wh"], 0)
        # Remaining-until-tomorrow includes today's remainder plus tomorrow's daily forecast.
        self.assertEqual(self.devices[1].sValue, "11.900")
        self.assertEqual(self.devices[2].sValue, "5.500")
        self.assertEqual(self.devices[REMAINING_TODAY_DETAIL_UNIT].sValue, "6.400")
        self.now = datetime(2026, 10, 15, 13, 5)
        app.poll()  # Adds the saved 13:00 forecast (1300 Wh).
        self.assertEqual(app.counter_state["total_wh"], 1300)
        self.assertEqual(self.devices[FORECAST_ENERGY_COUNTER_UNIT].sValue, "1400;1300")
        app.poll()
        self.assertEqual(app.counter_state["total_wh"], 1300)

    def test_pending_hour_and_total_survive_restart(self):
        app = self.make_app()
        app.poll()
        self.now = datetime(2026, 10, 15, 13, 5)
        app.poll()
        self.assertEqual(app.counter_state["total_wh"], 1300)
        restored = self.make_app()
        self.assertEqual(restored.counter_state["total_wh"], 1300)
        self.assertEqual(restored.counter_state["last_accounted_hour"], "2026-10-15T13:00:00")
        self.assertEqual(restored.counter_state["pending_hour"], "2026-10-15T14:00:00")

    def test_exact_hour_counts_current_hour_forecast(self):
        self.now = datetime(2026, 10, 15, 13, 0)
        app = self.make_app()
        app.poll()
        self.assertEqual(app.counter_state["total_wh"], 1300)
        self.assertEqual(app.counter_state["last_accounted_hour"], "2026-10-15T13:00:00")


if __name__ == "__main__":
    unittest.main()
