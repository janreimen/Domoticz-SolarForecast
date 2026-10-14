#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Domoticz plugin entry point. Business logic lives in solarforecast/."""

"""
<plugin key="SolarForecast"
        name="Solar Forecast"
        author="Jan Reimen"
        version="0.0.2"
        externallink="https://github.com/janreimen/Domoticz-SolarForecast">
    <description>
        <h2>Solar Forecast</h2>
        Forecasts photovoltaic energy remaining before midnight and the full-day
        forecast for tomorrow using forecast.solar. Configure via the .env file.
    </description>
</plugin>
"""

import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent
if str(PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(PLUGIN_DIR))

try:
    import Domoticz  # type: ignore
except ImportError:  # Offline development/test support only.
    class _DeviceStub:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.nValue = 0
            self.sValue = ""
        def Create(self):
            pass
        def Update(self, nValue=0, sValue="", Image=0, Options=None):
            self.nValue = nValue
            self.sValue = sValue
    class _DomoticzStub:
        @staticmethod
        def Log(message): print("LOG:", message)
        @staticmethod
        def Error(message): print("ERROR:", message)
        @staticmethod
        def Debug(message): print("DEBUG:", message)
        @staticmethod
        def Debugging(level): pass
        @staticmethod
        def Device(**kwargs): return _DeviceStub(**kwargs)
    Domoticz = _DomoticzStub()

from solarforecast.app import SolarForecastApp

Parameters = globals().get("Parameters", {})
Settings = globals().get("Settings", {})
Devices = globals().get("Devices", {})


def _devices():
    return globals().get("Devices", Devices)


def _settings():
    return globals().get("Settings", Settings)


_plugin = SolarForecastApp(Domoticz, _devices, _settings, PLUGIN_DIR)


def onStart():
    _plugin.on_start()


def onStop():
    _plugin.on_stop()


def onHeartbeat():
    _plugin.on_heartbeat()


def onCommand(Unit, Command, Level, Color):
    _plugin.on_command(Unit, Command, Level, Color)
