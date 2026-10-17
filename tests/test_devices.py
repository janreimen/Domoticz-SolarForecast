import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from solarforecast.devices import (
    DEVICE_DEFINITIONS, FORECAST_ENERGY_COUNTER_UNIT, ensure_devices, update_unit,
)


class ReadOnlyDevice:
    def __init__(self, n_value=0, s_value=""):
        self._n_value = n_value
        self._s_value = s_value
        self.calls = []

    @property
    def nValue(self): return self._n_value
    @property
    def sValue(self): return self._s_value

    def Update(self, nValue, sValue):
        self.calls.append((nValue, sValue))
        self._n_value = nValue
        self._s_value = sValue


class DeviceUpdateTests(unittest.TestCase):
    def setUp(self):
        self.logs = []
        self.log = lambda level, message: self.logs.append((level, message))

    def test_uses_update_method_for_read_only_properties(self):
        device = ReadOnlyDevice()
        update_unit(None, {1: device}, 1, "3.250", self.log)
        self.assertEqual(device.calls, [(0, "3.250")])
        self.assertEqual(device.sValue, "3.250")

    def test_skips_unchanged_value(self):
        device = ReadOnlyDevice(0, "3.250")
        update_unit(None, {1: device}, 1, "3.250", self.log)
        self.assertEqual(device.calls, [])

    def test_force_update_records_unchanged_value(self):
        device = ReadOnlyDevice(0, "3.250")
        update_unit(None, {1: device}, 1, "3.250", self.log, force=True)
        self.assertEqual(device.calls, [(0, "3.250")])

    def test_counter_is_native_kwh_generation_meter(self):
        definition = next(row for row in DEVICE_DEFINITIONS if row[0] == FORECAST_ENERGY_COUNTER_UNIT)
        self.assertEqual(definition[1], "Forecast Energy Return Counter")
        self.assertEqual(definition[2], "kWh")
        self.assertEqual(definition[3]["AddDBLogEntry"], "true")

    def test_ensure_devices_creates_counter_as_generation(self):
        class FakeDevice:
            def __init__(self, **kwargs): self.kwargs = kwargs
            def Create(self): created.append(self.kwargs)
        class FakeDomoticz:
            def Device(self, **kwargs): return FakeDevice(**kwargs)
        created = []
        ensure_devices(FakeDomoticz(), {})
        counter = next(d for d in created if d["Unit"] == FORECAST_ENERGY_COUNTER_UNIT)
        self.assertEqual(counter["Name"], "Forecast Energy Return Counter")
        self.assertEqual(counter["TypeName"], "kWh")
        self.assertEqual(counter["Switchtype"], 4)

    def test_missing_device_is_logged(self):
        update_unit(None, {}, 1, "3.250", self.log)
        self.assertTrue(self.logs)
        self.assertEqual(self.logs[0][0], "WARNING")


if __name__ == "__main__":
    unittest.main()
