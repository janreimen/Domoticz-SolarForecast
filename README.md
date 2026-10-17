# Domoticz Solar Forecast

- **Maintainer / project owner:** Jan Reimen ([`@janreimen`](https://github.com/janreimen))
- **Repository:** https://github.com/janreimen/Domoticz-SolarForecast
- **Latest stable release:** `0.0.4`
- **Development target:** `0.0.5`

Domoticz Solar Forecast is a modular Python plugin for [Domoticz](https://www.domoticz.com/) that retrieves photovoltaic (PV) production forecasts from [forecast.solar](https://forecast.solar/) and exposes forecast estimates as Domoticz devices.

The plugin supports single-array and multi-array PV installations, including arrays with different orientations, inclinations, panel counts, and rated panel power.

**Important:** Forecast values are estimates, not measurements of actual PV production and not guarantees of future production.

## Features

- Forecast energy remaining until the end of today.
- Forecast energy remaining across today and tomorrow.
- Full-day forecast for tomorrow.
- Forecast energy for the next complete clock-hour interval.
- Status information showing the most recent update result.
- Single-array and multi-array PV configurations.
- Independent panel orientation, inclination, panel count, and rated power for each array.
- Automatic creation and updating of Domoticz devices.
- Configuration through environment variables and an optional `.env` file.
- Optional forecast.solar API key.
- Modular implementation and automated offline tests.
- Development work towards retaining forecast history and improving historical forecast analysis in `0.0.5`.

## Devices

The development branch may contain additional devices compared with the stable `0.0.4` release. The following table describes the intended device roles while preserving existing unit IDs wherever possible.

| Unit | Device name | Meaning | Data type |
| --- | --- | --- | --- |
| 1 | Forecast Remaining (Today + Tomorrow) | Forecast energy remaining from now until the end of tomorrow | Forecast energy, kWh |
| 2 | Forecast Tomorrow | Forecast energy for the complete next calendar day | Forecast energy, kWh |
| 3 | Forecast Status | Latest update status and last successful update time | Text |
| 4 | Forecast Next Full Hour | Forecast energy for the next complete clock-hour interval | Forecast energy, kWh |
| 5 | Cumulative Forecast Energy | Cumulative forecast-related value; its calculation and counter semantics must be verified before use | Forecast-related value |
| 6 | Forecast Remaining Today | Forecast energy remaining from now until local midnight | Forecast energy, kWh |

Device availability depends on the branch and version installed. Check the device definitions in `solarforecast/devices.py` and the calculations in `solarforecast/forecast.py` before relying on a device in an automation.

Forecast values must not be treated as actual measured production, instantaneous power, irradiance, or financial earnings.

Do not interpret an unavailable forecast as a genuine zero-production forecast. Check the Status device and Domoticz logs before using forecast values in automations.

## Requirements

- Domoticz with Python plugin support enabled.
- A Python version supported by the installed Domoticz version.
- Network access to the forecast.solar API.
- Valid site coordinates and PV configuration.

The current implementation uses the Python standard library. No additional third-party Python packages are required by the current code.

## Installation

1. Back up the existing plugin directory and configuration.
2. Stop Domoticz before replacing plugin files.
3. Clone the repository into the Domoticz plugins directory:

   ```sh
   cd /srv/domoticz/plugins
   git clone https://github.com/janreimen/Domoticz-SolarForecast.git
   cd Domoticz-SolarForecast
