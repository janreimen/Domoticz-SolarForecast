# Domoticz Solar Forecast

- **Maintainer / project owner:** Jan Reimen ([`@janreimen`](https://github.com/janreimen))
- **Canonical repository:** https://github.com/janreimen/Domoticz-SolarForecast
- **Current version:** `0.0.4`

A modular [Domoticz](https://www.domoticz.com/) Python plugin that retrieves photovoltaic (PV) production forecasts from [forecast.solar](https://forecast.solar/) and exposes useful energy estimates as Domoticz devices.

> **Release:** `0.0.4` — supports multiple panel groups with different orientations and panel wattages. This is forecast data, not a meter reading or a guarantee of production.

## Features

- Forecast energy remaining today, strictly capped at local midnight.
- A separate full-day forecast for tomorrow.
- Forecast energy for the next complete clock-hour block (e.g. at 17:44, the 18:00–19:00 hour).
- Current forecast interval is prorated when the current time falls within it.
- Independent status device to help identify unavailable/stale forecast data.
- `.env`-based configuration; process environment variables take precedence.
- Modular implementation and offline unit tests.
- Optional forecast.solar API key.
- Multiple PV panel groups with independent tilt, compass orientation, panel count, and panel wattage; forecasts are requested per group and summed.

## Devices

| Unit | Device name | Meaning | Data meaning |
| --- | --- | --- | --- |
| 1 | Remaining Today | Estimated PV energy from now until midnight | Forecast energy, kWh |
| 2 | Tomorrow Forecast | Estimated PV energy for tomorrow's calendar day | Forecast energy, kWh |
| 3 | Status | Most recent update/result status | Text |
| 4 | Next Hour Forecast | Estimated PV energy for the next full clock hour | Forecast energy, kWh |

The numeric devices represent forecast energy, not actual generated energy, instantaneous power, irradiance, or money. Do not connect them to a cumulative energy counter as if they were meter readings. Check the Status device before using forecast values in automations. If a forecast is unavailable, do not assume a numeric zero means a genuine zero-production forecast.

## Requirements

- Domoticz with Python plugin support enabled.
- Python 3 supported by your Domoticz installation (the code uses the standard library).
- Network access to the forecast.solar API.
- Valid site coordinates and panel configuration.

No third-party Python packages are required by the current implementation.

## Installation

1. Back up your current plugin directory and configuration.
2. Stop Domoticz before replacing plugin files.
3. Copy this repository into the Domoticz plugins directory, for example:

   ```sh
   cd /srv/domoticz/plugins
   git clone https://github.com/janreimen/Domoticz-SolarForecast.git Domoticz-SolarForecast
   cd Domoticz-SolarForecast
   ```

   Replace `https://github.com/janreimen/Domoticz-SolarForecast.git` with the URL of the repository you are using. If you already have a clone, use the appropriate branch/tag and back up local changes before updating.
4. Create a local configuration file if one does not already exist:

   ```sh
   cp .env.example .env
   nano .env
   chmod 600 .env
   ```
5. Ensure the operating-system account running Domoticz can read `.env` and the plugin files.
6. Run the offline checks:

   ```sh
   python3 -m unittest discover -s tests -v
   python3 -m compileall -q plugin.py solarforecast
   ```
7. Restart Domoticz, add the Solar Forecast hardware/plugin through the Domoticz UI, and inspect the Domoticz log and Status device.

See [Configuration](docs/CONFIGURATION.md), [Troubleshooting](docs/TROUBLESHOOTING.md), and [Architecture](docs/ARCHITECTURE.md).

## Configuration at a glance

Copy `.env.example` to `.env` and adjust values for your installation.

| Variable | Default | Description |
| --- | --- | --- |
| `LATITUDE` | blank | Decimal latitude; blank uses Domoticz location settings |
| `LONGITUDE` | blank | Decimal longitude; blank uses Domoticz location settings |
| `PANEL_DECLINATION` | `45` | Panel tilt; slash-separated per group in multi-array mode |
| `PANEL_AZIMUTH` | `0` | Legacy mode: forecast.solar convention. Multi-array mode: compass bearings 0=N, 90=E, 180=S, 270=W |
| `PANEL_AMOUNT` | blank | Number of panels per group, slash-separated; required for multi-array mode |
| `PANEL_UNIQUE_POWER` | blank | Rated power per panel in watts, slash-separated; required for multi-array mode |
| `PANEL_PEAK_POWER_KWP` | `4.8` | Legacy single-array peak power. In multi-array mode, calculated from panel counts and wattages |
| `API_KEY` | blank | Optional forecast.solar API key |
| `POLL_INTERVAL_MINUTES` | `10` | Poll interval; minimum 5 minutes |
| `HTTP_TIMEOUT_SECONDS` | `20` | Maximum wait for an API response |
| `LOG_LEVEL` | `INFO` | `ERROR`, `WARNING`, `INFO`, `DEBUG`, or `TRACE` |

See [Configuration](docs/CONFIGURATION.md) for validation, precedence, multi-array examples, and azimuth conventions. Never commit `.env`, API keys, logs containing private data, or site-specific credentials.

## Midnight boundary and time handling

The remaining-today calculation uses the host's local time and never includes forecast intervals belonging to tomorrow. The current interval is prorated where possible. The Next Hour Forecast is the next complete clock-hour block, not a rolling 60-minute window: at 17:44 it covers 18:00–19:00. Tomorrow's estimate is taken from the API's daily forecast for tomorrow, not by adding today's remaining energy. Forecast availability and granularity depend on the upstream service and account plan.

## Community and support

- Read [FAQ](docs/FAQ.md), [Troubleshooting](docs/TROUBLESHOOTING.md), and the [Development Guide](docs/DEVELOPMENT.md) first.
- Report defects using the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).
- Suggest enhancements using the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).
- Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. See [Governance](GOVERNANCE.md) for project decision-making.
- Security-sensitive reports should follow [SECURITY.md](SECURITY.md), not a public issue.
- Community participation follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Credits and license

This project builds on the Domoticz SolarForecast plugin by [Jan-Jaap Kostelijk](https://github.com/JanJaapKo/SolarForecast), which is published under the GNU General Public License v3.0. See [LICENSE](LICENSE) for the license text and [NOTICE.md](NOTICE.md) for attribution notes. `forecast.solar` is an independent third-party service and is not affiliated with this plugin's maintainers.

## Release and compatibility notes

This release is `0.0.4`. Treat it as an early release: test it on a non-production Domoticz instance before relying on it for automations. Offline tests do not replace integration testing against your exact Domoticz version and a live API response. See [Release Process](docs/RELEASING.md).
