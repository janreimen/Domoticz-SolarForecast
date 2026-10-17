# Changelog

All notable user-facing changes to Domoticz-SolarForecast are documented in this file.

This project follows a simple, Keep a Changelog-inspired structure. Versions are listed in reverse chronological order.

## [0.0.5] - 2026-10-17

### Added

- Added forecast-history tracking through the cumulative forecast energy counter.
- Added persistent counter state to retain accumulated forecast energy and hourly accounting information across plugin restarts.
- Added pending-hour tracking so an hourly forecast can be saved and accounted for when the corresponding hour begins.
- Added protection against counting the same forecast hour more than once.
- Added automated tests for forecast-counter accumulation, exact-hour accounting, and restoration of counter state after restart.
- Expanded device tests for Domoticz device updates, counter configuration, and device unit ID uniqueness.
- Expanded plugin tests for multi-array configuration, forecast aggregation, and time-boundary behaviour.

### Changed

- Refined the test suite for device handling, forecast calculations, API responses, and multi-array PV configurations.
- Updated support and security documentation for development-version troubleshooting, diagnostic information, responsible vulnerability reporting, and handling of sensitive configuration data.
- Clarified that forecast estimates and cumulative forecast values are not actual PV meter readings or verified financial earnings.

### Notes

- The cumulative forecast energy counter represents forecast-derived energy, not measured PV production.
- Hourly accounting depends on the forecast data available when the relevant hour is processed.
- Forecast history and accumulated values should be checked against the implementation and live Domoticz behaviour before being used for reporting.
- Run the complete offline test suite before installing this version on a production Domoticz instance.

## [0.0.4] - 2026-10-15

### Added

- Multi-array PV configuration using slash-separated panel tilt, compass azimuth, panel count, and per-panel wattage.
- Independent forecast.solar request for each panel group, with period and daily energy summed by timestamp.
- Automatic total peak-power calculation from panel counts and rated wattage.
- Backward-compatible support for existing single-array configuration.

### Changed

- Multi-array azimuths use standard compass bearings (0° north, 90° east, 180° south, 270° west) and are converted internally to the forecast.solar azimuth convention.
- Updated package metadata and documentation to version 0.0.4.

## [0.0.3] - 2026-10-14

### Added

- Added the `Next Hour Forecast` kWh sensor (Domoticz unit 4).
- The sensor estimates energy for the next complete clock-hour block, not a rolling 60-minute window. For example, at 17:44 it forecasts 18:00–19:00.
- Added fixed-time unit tests for next-hour boundary behaviour.

### Changed

- Updated plugin metadata, package version, API User-Agent, and current-release documentation to `0.0.3`.

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
- HTTP timeout and error handling, plus offline unit tests.
- Community documentation, contribution guidance, security policy, support guide, issue templates, and automated test workflow.

### Notes

- Forecasts are estimates and are not actual meter readings or financial earnings.
- Live Domoticz integration should be validated on a test instance before production use.
