# Changelog

All notable user-facing changes for this project are documented here. This project uses a simple Keep a Changelog-inspired structure.

## [0.0.2] - 2026-10-14

### Fixed

- Pass device values to Domoticz `Update()` instead of assigning read-only `nValue`/`sValue` properties.

### Changed

- Set the plugin version and API User-Agent to `0.0.2`.
- Set Jan Reimen as project maintainer and point the plugin metadata to the canonical repository.
- Update current-version references in the documentation and issue templates.
- Exclude Python bytecode/cache files from the source package.

## [0.0.1] - 2026-10-14

### Added

- Modular plugin structure with focused configuration, API, forecast, device, and application modules.
- `.env` configuration with validation and process-environment precedence.
- Remaining Today energy forecast with local-midnight cutoff and current-interval prorating.
- Separate Tomorrow Forecast daily energy sensor.
- Status device for the most recent refresh result.
- HTTP timeout/error handling and offline unit tests.
- Community documentation, contribution guidance, security policy, support guide, issue templates, and automated test workflow.

### Notes

- Forecasts are estimates and are not actual meter readings or financial earnings.
- Live Domoticz integration should be validated on a test instance before production use.
