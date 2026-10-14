# Troubleshooting

## Plugin does not appear in Domoticz

- Confirm Python plugin support is enabled in Domoticz.
- Check the directory name and ensure `plugin.py` is at the plugin root.
- Ensure the Domoticz service account can read the files.
- Inspect the Domoticz log for import or syntax errors.
- Run `python3 -m compileall -q plugin.py solarforecast` from the plugin directory.

## Configuration errors at startup

- Check `.env` syntax: use `NAME=value`, one setting per line.
- Confirm latitude and longitude are numeric and within range.
- Confirm panel tilt and peak power are valid.
- Check that the Domoticz location is set if coordinate fields are blank.
- Verify the file is readable by the account that runs Domoticz.

## API request fails or rate limit is reached

- Confirm the host has internet access and can reach `https://api.forecast.solar/`.
- Check system date/time and TLS certificate support.
- Verify API key validity and the plan's request limits.
- Increase `HTTP_TIMEOUT_SECONDS` only if network latency justifies it.
- Do not reduce the poll interval below five minutes; consider increasing it if your provider plan has a low request allowance.
- Never include a credential-bearing URL or API key in a public log excerpt.

## Forecast value appears to be zero or missing

- Check the Status device first; a zero may not mean a valid forecast when the API data is unavailable.
- Verify site coordinates, panel geometry, and peak power.
- Check whether the API response includes the relevant daily and period data for the current date.
- Compare the API response timestamp and the host's local time/time zone.
- Remember that a forecast is an estimate and can change with each refresh.

## Values cross midnight unexpectedly

- Record the local time and timezone, plugin version, and a redacted sample response.
- Confirm the system clock is correct.
- Include a reproducible sample in an issue; never include API keys or precise home coordinates.

## Run local checks

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q plugin.py solarforecast
```

These checks do not verify live Domoticz device rendering or live provider behavior. Those require a separate test instance.
