# Roadmap

This document outlines the planned development of **Domoticz-SolarForecast**, a Domoticz plugin that retrieves solar production forecasts and exposes them as Domoticz devices.

The roadmap is indicative. Priorities may change based on bug reports, testing results, user feedback, and changes to the upstream forecast service.

## Current Development

### v0.0.5 — Forecast History and Reliability

**Goal:** Improve forecast tracking, persistence, and test coverage.

- [x] Support multiple PV arrays with individual orientation, tilt, panel count, and panel power.
- [ ] Track forecast-derived energy over time.
- [ ] Persist forecast-counter state across plugin restarts.
- [ ] Avoid counting the same forecast hour more than once.
- [ ] Handle polling failures and missing forecast periods reliably.
- [ ] Validate device names, units, and Domoticz meter semantics.
- [ ] Expand automated tests for forecast calculations and history tracking.
- [ ] Update documentation, installation instructions, and support information.
- [ ] Verify the complete test suite on the supported Domoticz environment.

**Release status:** In development. Mark this release complete only after implementation and tests have been verified.

## Planned Releases

### v0.0.6 — Forecast History Improvements

**Goal:** Make historical forecast information more useful for troubleshooting and analysis.

Potential improvements:

- [ ] Improve the structure and readability of stored forecast history.
- [ ] Define how long historical data should be retained.
- [ ] Handle missing, stale, or revised forecast data.
- [ ] Improve diagnostics for forecast changes between polling cycles.
- [ ] Document the difference between predicted energy and measured PV production.

### v0.0.7 — Configuration and Diagnostics

**Goal:** Make configuration easier to understand and diagnose.

Potential improvements:

- [ ] Improve validation of single-array and multi-array configuration.
- [ ] Provide clear errors for invalid array counts, orientations, tilts, and panel power.
- [ ] Improve logging for API errors, timeouts, and malformed responses.
- [ ] Document configuration examples for common PV installations.
- [ ] Review compatibility with supported Domoticz and Python versions.

### v0.1.0 — Stable Feature Set

**Goal:** Establish a well-tested baseline for regular use.

Planned release criteria:

- [ ] Automated tests cover the main forecast and device-update paths.
- [ ] Restart and state-restoration behaviour is tested.
- [ ] Duplicate forecast accounting is prevented.
- [ ] Configuration errors produce actionable messages.
- [ ] Device names, units, and counter semantics are documented.
- [ ] Installation and upgrade procedures are documented.
- [ ] A release has been tested in a real Domoticz installation.

The exact scope of v0.1.0 will depend on feedback and testing results.

## Longer-Term Ideas

The following ideas have no committed release date:

- [ ] Compare historical forecasts with measured PV production from another system.
- [ ] Provide better insight into forecast accuracy over time.
- [ ] Improve diagnostics for individual PV arrays.
- [ ] Add optional export or integration mechanisms if there is a clear use case.
- [ ] Review opportunities to reduce unnecessary API requests.

These ideas will be considered only where they add practical value without making the plugin unnecessarily complex.

## Out of Scope

Unless a specific use case justifies a change, the project will not:

- Treat forecast estimates as measured production.
- Require a paid API key where the upstream service supports access without one.
- Enable unrelated remote-control functionality.
- Introduce unnecessary external dependencies.
- Promise compatibility with untested Domoticz versions.

## Contributing

Bug reports, feature requests, and tested improvements are welcome.

Before proposing a feature, please check the existing issues and explain the problem it solves. Bug reports should include the plugin version, relevant redacted logs, configuration details that are safe to share, and steps to reproduce the issue.

See [SUPPORT.md](SUPPORT.md) for support guidance and [SECURITY.md](SECURITY.md) for vulnerability reporting.

## Versioning

The project uses versioned releases to communicate changes. The roadmap is not a guarantee of delivery dates or feature availability.

See [CHANGELOG.md](CHANGELOG.md) for implemented changes and release notes.

