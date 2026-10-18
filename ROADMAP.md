# Roadmap

This roadmap outlines possible future work for **Domoticz-SolarForecast**. Priorities may change based on testing, bug reports, upstream API changes, and user feedback. It is indicative, not a delivery-date commitment.

## Current development — v0.0.5

**Goal:** Improve forecast tracking, persistence, device clarity, and test coverage.

- [x] Support multiple PV arrays with individual orientation, tilt, panel count, and panel power.
- [ ] Verify cumulative forecast-energy tracking over time.
- [ ] Verify that counter state and the pending hour survive plugin restarts.
- [ ] Verify duplicate-hour protection at hour boundaries.
- [ ] Handle polling failures and missing forecast periods reliably.
- [ ] Validate device names, units, and Domoticz meter semantics.
- [ ] Expand automated tests for forecast calculations and history tracking.
- [ ] Verify the complete test suite and test on a real Domoticz installation.

Release status: in development until the implementation and tests have been verified.

## v0.0.6 — Forecast history improvements

Potential goals:

- [ ] Improve the structure and readability of stored forecast history.
- [ ] Define a retention policy for historical data.
- [ ] Handle missing, stale, or revised forecast data.
- [ ] Improve diagnostics for changes between forecast polling cycles.
- [ ] Document forecast estimates versus measured PV production.

## v0.0.7 — Configuration and diagnostics

Potential goals:

- [ ] Improve validation for single-array and multi-array configurations.
- [ ] Provide actionable errors for invalid panel counts, orientations, tilts, and power values.
- [ ] Improve logging for API errors, timeouts, and malformed responses.
- [ ] Add configuration examples for common PV installations.
- [ ] Review compatibility with supported Domoticz and Python versions.

## v0.1.0 — Stable feature set

Potential release criteria:

- [ ] Automated tests cover the main forecast and device-update paths.
- [ ] Restart and state-restoration behaviour is tested.
- [ ] Duplicate forecast accounting is prevented.
- [ ] Configuration errors produce actionable messages.
- [ ] Device names, units, and counter semantics are documented.
- [ ] Installation and upgrade procedures are documented.
- [ ] The release has been tested in a real Domoticz installation.

## Longer-term ideas

- [ ] Compare historical forecasts with measured PV production from another system.
- [ ] Provide insight into forecast accuracy over time.
- [ ] Improve diagnostics for individual PV arrays.
- [ ] Consider optional export/integration mechanisms where there is a clear use case.
- [ ] Reduce unnecessary API requests where possible.

## Project principles

- Forecast estimates must not be presented as measured production.
- Do not introduce unnecessary external dependencies.
- Do not promise compatibility with untested Domoticz versions.
- Keep configuration and logs safe for users to share after redaction.

## Contributing

Bug reports, feature requests, and tested improvements are welcome. See [SUPPORT.md](SUPPORT.md), [SECURITY.md](SECURITY.md), and [CONTRIBUTING.md](CONTRIBUTING.md). Implemented changes belong in [CHANGELOG.md](CHANGELOG.md).
