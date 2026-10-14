# Development guide

## Local environment

The plugin currently depends on the Python standard library. Use the same Python major/minor version as the target Domoticz runtime when investigating compatibility issues.

```sh
python3 --version
python3 -m unittest discover -s tests -v
python3 -m compileall -q plugin.py solarforecast
```

## Where to change code

- Configuration parsing and validation: `solarforecast/config.py`
- API URL and HTTP handling: `solarforecast/api.py`
- Forecast parsing and date calculations: `solarforecast/forecast.py`
- Domoticz device creation and updates: `solarforecast/devices.py`
- Plugin lifecycle and orchestration: `solarforecast/app.py`
- Domoticz entry-point metadata/callbacks: `plugin.py`

## Testing forecast logic

Use fixed `datetime` instances and synthetic API payloads. Cover at least:

- current interval before, during, and after the current time;
- midnight and next-day boundary behavior;
- missing or malformed API fields;
- API errors and unavailable daily totals;
- invalid configuration and location fallback.

Avoid real API calls in unit tests. Redact credentials and site-specific details in any fixture that originated from a real installation.

## Logging

Logs should explain actionable failures without exposing API keys, full credential-bearing URLs, or unnecessary personal/location data. Do not swallow errors silently; report a useful status and keep the plugin lifecycle stable.

## Domoticz integration testing

Before production use, test plugin creation, restart behavior, heartbeat polling, device updates, removal/recreation, and the Domoticz log on a disposable/test instance. Unit tests alone cannot establish integration compatibility.
