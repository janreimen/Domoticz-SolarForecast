# Support

Domoticz-SolarForecast is a community-maintained plugin provided on a best-effort basis.

## Before asking for help

1. Read the [README](README.md), [FAQ](docs/FAQ.md), and [Troubleshooting](docs/TROUBLESHOOTING.md).
2. Record the plugin version, Domoticz version, and Python version.
3. Run the offline checks from the plugin directory:

   ```sh
   python3 -m unittest discover -s tests -v
   python3 -m compileall -q plugin.py solarforecast tests
   ```

4. Check the Domoticz log around plugin startup and a forecast refresh.
5. Include the relevant configuration keys and a minimal reproduction, but redact API keys, account identifiers, precise home coordinates, public IPs, and other private details. Never post `.env` or unredacted logs.

## Where to ask

- **Bug:** open an issue using the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).
- **Enhancement:** use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).
- **Usage question:** use the [question template](.github/ISSUE_TEMPLATE/question.md), or a discussion if GitHub Discussions is enabled.
- **Security concern:** follow [SECURITY.md](SECURITY.md); do not post vulnerability details publicly.

Please state expected versus actual behaviour and whether the issue is reproducible with the current development version. Support is best-effort; there is no guaranteed response time or long-term support promise for older releases.
