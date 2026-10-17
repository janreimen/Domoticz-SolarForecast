# Configuration

The plugin reads a `.env` file from the plugin directory. Variables in the process environment take precedence over values in `.env`. Keep `.env` private and never commit it.

## Settings

| Variable | Meaning |
|---|---|
| `LATITUDE` | Decimal latitude, -90 through 90. Blank uses Domoticz's configured location. |
| `LONGITUDE` | Decimal longitude, -180 through 180. Blank uses Domoticz's configured location. |
| `PANEL_DECLINATION` | Panel tilt in degrees, 0 through 90. In multi-array mode, slash-separated values, one per group. |
| `PANEL_AZIMUTH` | In legacy single-array mode, forecast.solar convention: 0=south, -90=east, +90=west. In multi-array mode, slash-separated compass bearings: 0=north, 90=east, 180=south, 270=west. |
| `PANEL_AMOUNT` | Required for multi-array mode; slash-separated number of panels in each group. |
| `PANEL_UNIQUE_POWER` | Required for multi-array mode; slash-separated rated power of each panel in watts. |
| `PANEL_PEAK_POWER_KWP` | Legacy single-array installed peak power in kWp. In multi-array mode the total is calculated automatically and this setting is ignored. |
| `API_KEY` | Optional API key supplied by forecast.solar. |
| `POLL_INTERVAL_MINUTES` | Poll interval; integer, minimum 5 minutes. Respect provider rate limits. |
| `HTTP_TIMEOUT_SECONDS` | Positive HTTP timeout in seconds. |
| `LOG_LEVEL` | `ERROR`, `WARNING`, `INFO`, `DEBUG`, or `TRACE`. |

## Multiple panel orientations

Use one slash-separated entry per distinct panel group. The four lists must have exactly the same number of entries and correspond by position. The plugin requests a forecast for each group separately and sums the returned energy forecasts by timestamp/day. Total peak power is calculated as `sum(panel count × panel watts) / 1000`.

Example for 22 south-facing panels rated at 310 W, 5 east-facing panels rated at 305 W, and 5 west-facing panels rated at 480 W:

```dotenv
PANEL_DECLINATION=30/45/30
PANEL_AZIMUTH=180/90/270
PANEL_AMOUNT=22/5/5
PANEL_UNIQUE_POWER=310/305/480
PANEL_PEAK_POWER_KWP=
```

This example totals 10.745 kWp. Note that `PANEL_AZIMUTH` uses compass bearings in multi-array mode; the plugin converts them to forecast.solar's convention internally. `PANEL_DECLINATION` is tilt from horizontal (0° horizontal, 90° vertical). Each group produces a separate API request, so make sure your forecast.solar plan/rate limit supports the number of groups and configured polling frequency.

Existing single-array configurations remain supported using numeric `PANEL_DECLINATION`, `PANEL_AZIMUTH`, and `PANEL_PEAK_POWER_KWP` values. In that legacy mode, azimuth keeps the old forecast.solar convention.

## Setup

```sh
cp .env.example .env
nano .env
chmod 600 .env
```

Blank coordinates are resolved from Domoticz's location settings. If Domoticz's configured location is missing or malformed, specify explicit coordinates. Never share exact coordinates or API keys in public issues unless necessary.
