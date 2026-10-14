# Configuration

The plugin reads a `.env` file from the plugin directory. Variables in the process environment take precedence over values in `.env`. Keep `.env` private and never commit it.

## Settings

| Variable | Default | Valid values / meaning |
| --- | --- | --- |
| `LATITUDE` | blank | Decimal degrees, -90 through 90. Blank uses Domoticz's configured location. |
| `LONGITUDE` | blank | Decimal degrees, -180 through 180. Blank uses Domoticz's configured location. |
| `PANEL_DECLINATION` | `45` | Panel tilt in degrees, 0 through 90. |
| `PANEL_AZIMUTH` | `0` | forecast.solar convention: 0 south, -90 east, +90 west; see provider documentation for full range. |
| `PANEL_PEAK_POWER_KWP` | `4.8` | Positive installed peak DC power in kWp. |
| `API_KEY` | blank | Optional API key supplied by forecast.solar. |
| `POLL_INTERVAL_MINUTES` | `10` | Integer interval; minimum 5 minutes. Respect provider rate limits. |
| `HTTP_TIMEOUT_SECONDS` | `20` | Positive HTTP timeout in seconds. |
| `LOG_LEVEL` | `INFO` | `ERROR`, `WARNING`, `INFO`, `DEBUG`, or `TRACE`. |

## Setup

```sh
cp .env.example .env
nano .env
chmod 600 .env
```

Blank coordinates are resolved from Domoticz's location settings. If Domoticz's configured location is missing or malformed, specify explicit coordinates. Confirm panel tilt, azimuth, and peak capacity against your installation.

## Security and privacy

- Do not commit `.env`; `.gitignore` excludes it.
- Restrict file access, for example with `chmod 600 .env`, and ensure the Domoticz service account can read it.
- Avoid sharing your exact coordinates in public issues unless necessary.
- API keys can be subject to service plan quotas. Never paste them into issue reports or screenshots.
- Do not enable verbose logging in public environments without checking what is logged.
