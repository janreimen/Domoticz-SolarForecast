# Domoticz Solar Forecast

- **Maintainer / project owner:** Jan Reimen ([@janreimen](https://github.com/janreimen))
- **Canonical repository:** https://github.com/janreimen/Domoticz-SolarForecast
- **Version:** `0.0.5`

A modular [Domoticz](https://www.domoticz.com/) Python plugin that retrieves photovoltaic (PV) production forecasts from [forecast.solar](https://forecast.solar/) and exposes useful energy estimates as Domoticz devices.

> **Release 0.0.5:** Builds on multi-array PV forecasting with forecast-history tracking and a cumulative forecast-energy counter. Forecast values are estimates, not measured production or a guarantee of energy generation.

## Features

- Forecast PV energy remaining today, capped at local midnight.
- Separate full-day forecast for tomorrow.
- Forecast energy for the next complete clock-hour block. For example, at 17:44, the forecast covers 18:00–19:00.
- Prorating of the current forecast interval where supported by available forecast data.
- Status device showing the most recent refresh result.
- Configuration through `.env`, with process environment variables taking precedence.
- Optional forecast.solar API key.
- Multi-array PV configurations with different panel tilts, orientations, panel counts, and panel wattages.
- Independent forecast requests for panel groups, with forecast results combined by timestamp.
- Automatic total peak-power calculation in multi-array mode.
- Forecast-history accounting through a cumulative forecast-energy counter.
- Persistent history-keeper state intended to preserve accumulated values and hourly accounting information across plugin restarts.
- Offline unit tests for configuration, forecast calculations, device updates, multi-array aggregation, and history-keeper behaviour.

## Devices

| Unit | Device name | Meaning | Data interpretation |
| --- | --- | --- | --- |
| 1 | Forecast Remaining (Today + Tomorrow) | Estimated PV energy from now until the end of tomorrow, according to the current device definition | Forecast energy, kWh |
| 2 | Forecast Tomorrow | Estimated PV energy for tomorrow's calendar day | Forecast energy, kWh |
| 3 | Forecast Status | Most recent update or error status | Text |
| 4 | Forecast next hour | Estimated PV energy for the applicable complete clock-hour block | Forecast energy, kWh |
| 5 | Cumulative Forecast Energy | Accumulated forecast-derived energy tracked by the history keeper | Forecast accounting counter |
| 6 | Forecast Remaining Today | Estimated PV energy remaining today until local midnight | Forecast energy, kWh |

**Important:** confirm the exact meaning of Unit 1 against the current implementation before relying on it in automations. Unit 6 is the separate remaining-today estimate. The counter in Unit 5 is forecast-derived; it is not an actual PV production meter.

The cumulative counter is designed to track hourly forecast accounting rather than measured energy. Its accumulated value depends on the forecasts available and the accounting logic implemented by the plugin. Do not use it as a substitute for an actual generation meter or for financial reporting.

Check the Status device and the Domoticz log before using forecast values in automations. If a refresh fails, do not assume a numeric zero represents a genuine zero-production forecast.

## Requirements

- Domoticz with Python plugin support enabled.
- A Python version supported by your Domoticz installation.
- Network access to the forecast.solar API.
- Valid site coordinates and panel configuration.

The plugin is designed to use the Python standard library. Check `requirements.txt` and your installed version before installing additional packages.

## Installation

1. Back up the existing plugin directory and configuration.
2. Stop Domoticz before replacing plugin files.
3. Clone the repository or update an existing clone using the intended release tag or branch.

For a new clone:

```bash
cd /srv/domoticz/plugins
git clone https://github.com/janreimen/Domoticz-SolarForecast.git Domoticz-SolarForecast
cd Domoticz-SolarForecast
```

For an existing clone, preserve local changes and check out the intended version rather than blindly replacing the working directory.

4. Create a local configuration file if one does not already exist:

```bash
cp .env.example .env
nano .env
chmod 600 .env
```

5. Ensure the operating-system account running Domoticz can read the configuration and plugin files.
6. Run the offline tests and syntax checks:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q plugin.py solarforecast tests
```

7. Restart Domoticz, add or verify the Solar Forecast hardware through the Domoticz interface, and inspect the startup log and Status device.
8. Verify the forecast values and history-counter behaviour before using the new devices in production automations.

See [Configuration](docs/CONFIGURATION.md), [Troubleshooting](docs/TROUBLESHOOTING.md), and [Architecture](docs/ARCHITECTURE.md).

## Configuration at a glance

Copy `.env.example` to `.env` and adjust the settings for your installation.

| Variable | Default | Description |
| --- | --- | --- |
| `LATITUDE` | Blank | Decimal latitude; blank uses Domoticz location settings if supported by the implementation |
| `LONGITUDE` | Blank | Decimal longitude; blank uses Domoticz location settings if supported by the implementation |
| `PANEL_DECLINATION` | `45` | Panel tilt; slash-separated values for multiple panel groups |
| `PANEL_AZIMUTH` | `0` | Panel orientation; see the azimuth conventions below |
| `PANEL_AMOUNT` | Blank | Panel count per group; required for multi-array mode |
| `PANEL_UNIQUE_POWER` | Blank | Rated power per panel in watts; required for multi-array mode |
| `PANEL_PEAK_POWER_KWP` | `4.8` | Legacy single-array peak power; automatically calculated in multi-array mode |
| `API_KEY` | Blank | Optional forecast.solar API key |
| `POLL_INTERVAL_MINUTES` | `10` | Forecast polling interval; minimum 5 minutes |
| `HTTP_TIMEOUT_SECONDS` | `20` | Maximum wait for an API response |
| `LOG_LEVEL` | `INFO` | Logging verbosity: `ERROR`, `WARNING`, `INFO`, `DEBUG`, or `TRACE` |

Defaults and accepted values must match the `.env.example` and validation logic of the installed version. See [Configuration](docs/CONFIGURATION.md) for the complete reference.

### Single-array configuration

A single-array setup specifies the site location, panel tilt, orientation, and peak power. Existing single-array configurations should remain supported.

### Multi-array configuration

Multi-array mode allows different roof sections or installations to use different orientations, tilts, panel counts, and panel wattages.

For example, the following values represent three panel groups:

```dotenv
PANEL_DECLINATION=30/45/30
PANEL_AZIMUTH=180/90/270
PANEL_AMOUNT=22/5/5
PANEL_UNIQUE_POWER=310/305/480
PANEL_PEAK_POWER_KWP=
```

This example describes:

- 22 panels rated at 310 W each, facing south with a 30° tilt.
- 5 panels rated at 305 W each, facing east with a 45° tilt.
- 5 panels rated at 480 W each, facing west with a 30° tilt.

The resulting total nominal peak power is 10.745 kWp.

The multi-array lists must contain the same number of entries. In multi-array mode, the plugin requests forecasts for each panel group and combines results by timestamp.

### Azimuth conventions

Multi-array configuration uses compass bearings:

- `0`: North
- `90`: East
- `180`: South
- `270`: West

The plugin converts these bearings to the convention expected by forecast.solar. Legacy single-array configuration may use a different convention, so do not change existing azimuth values without checking the configuration documentation.

Never commit `.env`, API keys, credentials, or logs containing private information.

## Forecast timing and midnight boundaries

The remaining-today calculation uses the host's local time and must not include forecast intervals belonging to the next calendar day. The current interval may be prorated where the required data is available.

The `Next Hour Forecast` device represents a complete clock-hour interval rather than a rolling 60-minute window. For example, at 17:44, it represents 18:00–19:00. At exactly 17:00, the applicable interval begins at 17:00, as tested by the plugin.

The `Tomorrow Forecast` device uses the API's daily forecast for tomorrow rather than simply adding the remaining energy for today. Forecast availability, granularity, and limits depend on the upstream service and account plan.

## Forecast-history keeper and cumulative counter

Version 0.0.5 introduces forecast-history accounting intended to retain cumulative forecast-derived energy and hourly accounting state.

The history keeper is tested for:

- Saving a forecast for a future hourly interval.
- Accounting for the saved forecast when the hour begins.
- Avoiding duplicate accounting of the same hour.
- Restoring accumulated and pending-hour state after a restart.
- Handling the exact-hour boundary.

The counter represents forecast-derived values, not actual measured PV energy. Its value should not be interpreted as measured production, exported electricity, household consumption, or financial earnings.

Before relying on the counter, verify the current implementation in `solarforecast/app.py` and `solarforecast/devices.py`. In particular, confirm how state is persisted, how counter values are updated, and how missing forecast intervals are handled.

## Testing and troubleshooting

Run the complete offline test suite from the plugin directory:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q plugin.py solarforecast tests
```

If tests fail, resolve the failures before treating the version as release-ready. Offline tests do not replace integration testing against your specific Domoticz version and a live forecast.solar response.

When investigating problems:

1. Confirm the plugin version and Git branch or commit.
2. Check the Domoticz log during startup and forecast refresh.
3. Check the Status device for the latest result.
4. Validate the coordinates, panel configuration, and API key settings.
5. Confirm that the service account can read the configuration file.
6. Redact API keys, credentials, private addresses, and precise coordinates before sharing logs.

See [FAQ](docs/FAQ.md) and [Troubleshooting](docs/TROUBLESHOOTING.md).

## Community and support

- Read the [FAQ](docs/FAQ.md), [Troubleshooting Guide](docs/TROUBLESHOOTING.md), and [Development Guide](docs/DEVELOPMENT.md).
- Report defects using the repository's bug report template, if available.
- Suggest enhancements using the feature request template, if available.
- Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
- See [GOVERNANCE.md](GOVERNANCE.md) for project decision-making.
- Report security-sensitive issues according to [SECURITY.md](SECURITY.md), not through a public issue.
- Community participation follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Credits and license

This project builds on the Domoticz SolarForecast plugin by [Jan-Jaap Kostelijk](https://github.com/JanJaapKo/SolarForecast), published under the GNU General Public License v3.0. See [LICENSE](LICENSE) for the license text and [NOTICE.md](NOTICE.md) for attribution notes.

`forecast.solar` is an independent third-party service and is not affiliated with the plugin maintainer.

## Release and compatibility notes

Version `0.0.5` extends the multi-array implementation introduced in `0.0.4` with forecast-history accounting and associated tests.

Treat this early-stage version as requiring validation. Test on a non-production Domoticz instance before relying on it for automations. Check [CHANGELOG.md](CHANGELOG.md) for release history and [docs/RELEASING.md](docs/RELEASING.md) for the release procedure.
