# Architecture

Release `0.0.5` separates Domoticz integration from forecast logic to keep future changes maintainable.

## Modules

| File | Responsibility | Keep out of this module |
| --- | --- | --- |
| `plugin.py` | Domoticz XML metadata and lifecycle callback entry points | Forecast calculations and API parsing |
| `solarforecast/config.py` | `.env` and process-environment parsing, defaults, validation | HTTP requests and device updates |
| `solarforecast/api.py` | Forecast URL construction, HTTP request, JSON/error handling | Domoticz device state |
| `solarforecast/forecast.py` | Parsing forecast payloads and computing date-bounded energy estimates | Network calls and Domoticz imports |
| `solarforecast/devices.py` | Stable device unit definitions and safe create/update behavior | API requests and config parsing |
| `solarforecast/app.py` | Startup/shutdown, polling schedule, logging, and orchestration | Duplicated calculation logic |

## Data flow

1. Domoticz calls the entry point callbacks in `plugin.py`.
2. `app.py` loads validated settings from `config.py`.
3. At the configured interval, `api.py` requests a forecast from forecast.solar.
4. `forecast.py` validates the response and calculates remaining energy today, the next complete clock-hour energy, and tomorrow's daily energy.
5. `app.py` saves the next-hour forecast as a pending sample; when that forecast hour begins, it adds the sample once to a persistent cumulative Wh total.
6. `devices.py` updates the forecast units, native electricity counter, and status device.

## Forecast semantics

- Remaining Until Tomorrow 23:59 (unit 1): forecast energy from now through the end of tomorrow, computed as remaining energy today plus tomorrow's daily forecast when available.
- Forecast Tomorrow (unit 2): the API's daily forecast for the next local calendar date.
- Next Full Hour (unit 4): forecast energy during the next full clock-hour block (e.g. 18:00–19:00 when current time is 17:44); it is not a rolling 60-minute window.
- Forecast Energy Return Counter (unit 5): native Domoticz generated/returned-energy counter (`Switchtype=4`), not usage. Its power field is the next-hour forecast expressed as average W, and its cumulative energy field is the sum of one forecast sample per hour in Wh. This is an accumulated forecast, not measured household production. The pending forecast and total are saved in `.solarforecast_counter.json`.
- Remaining Today (unit 6): unit 1 minus unit 2, keeping the today-only forecast separately available.
- Status (unit 3): indicates the most recent successful/failed refresh so automations can distinguish missing data from a valid forecast.

Do not derive solar irradiance from forecast PV power or energy. Add irradiance only if a provider returns an actual irradiance field with a documented unit.

## Extension points

- **New provider:** create a provider client with a narrow interface and provider-specific response parsing; keep calculations independent where possible.
- **New sensor:** define stable unit metadata in `devices.py`, compute its value in a pure function, and cover it with tests.
- **New configuration option:** add defaulting and validation in `config.py`, document it in `.env.example` and the configuration docs, and test valid/invalid values.
- **New schedule behavior:** update `app.py` and test time transitions explicitly.

## Testing boundaries

Unit tests should use synthetic fixture payloads and fixed datetimes. Do not require a live API, a running Domoticz process, or real user credentials in the test suite. Integration tests against a real Domoticz instance are separate and should be documented as such.
