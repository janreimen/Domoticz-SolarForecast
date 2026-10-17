# Support

Domoticz-SolarForecast is a community-maintained plugin provided on a best-effort basis. Support is not guaranteed, and response times may vary.

## Before Asking for Help

Please complete these checks before opening an issue:

1. Read the [README](README.md), [FAQ](docs/FAQ.md), and [Troubleshooting Guide](docs/TROUBLESHOOTING.md).
2. Confirm the plugin version, Domoticz version, and Python version.
3. Run the offline test suite from the plugin directory:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

4. Check Python syntax:

   ```bash
   python3 -m compileall -q plugin.py solarforecast tests
   ```

5. Review the Domoticz log around plugin startup and at least one forecast refresh.
6. Check whether the problem is reproducible after restarting the plugin, where appropriate.

Do not include API keys, passwords, vehicle identification numbers, public IP addresses, account identifiers, precise home coordinates, or other private information in an issue or log excerpt. Redact sensitive values before sharing diagnostic output.

## Reporting an Issue

When opening an issue, include:

- The plugin version and the Git branch or commit, if applicable.
- Your Domoticz version and Python version.
- A clear description of the problem.
- The expected behaviour and the actual behaviour.
- The steps needed to reproduce the problem.
- Relevant, redacted Domoticz log messages.
- The results of the offline test suite and compilation checks, including any failures.

Please report one distinct problem per issue where practical.

## Where to Ask

- **Bug report:** Open a GitHub issue using the bug report template, if available.
- **Feature request:** Open a GitHub issue using the feature request template, if available.
- **Usage question:** Check the documentation first. If GitHub Discussions or a suitable question template is available, use it.
- **Security concern:** Follow the instructions in [SECURITY.md](SECURITY.md). Do not publish sensitive vulnerability details in a public issue.

Use the repository's available issue templates and discussion facilities where applicable.

## Supported Versions

The current development version may contain unfinished features or regressions. When reporting a problem on the development branch, identify the branch and commit so the issue can be reproduced.

Older releases may no longer receive fixes. If possible, check whether the problem also occurs on the latest stable release before reporting it.

## Expectations

This project is maintained on a best-effort basis. There is no guarantee of immediate responses, a particular resolution time, or continued support for older releases.

Contributions that include a reproducible test case are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.
