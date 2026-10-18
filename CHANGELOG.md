# Changelog

## [0.0.5] - 2026-10-17

### Added

- Added Unit 6, `Forecast Remaining Today`, derived as Unit 1 minus tomorrow's daily forecast.
- Persist the cumulative Wh total and pending forecast hour so a restart does not add the same hour twice.

### Changed

- Unit 1 is `Forecast Remaining (Today + Tomorrow)`; Unit 2 is `Forecast Tomorrow`; Unit 3 is `Forecast Status`; Unit 4 is `Forecast Next Full Hour`; Unit 5 is `Cumulative Forecast Energy`; Unit 6 is `Forecast Remaining Today`. Existing unit numbers remain unchanged.
- Configured Unit 5 as a native Domoticz generated/returned-energy counter (`Switchtype=4`), not an electricity-usage counter.
- Updated the status/log wording to report all four forecast values.
- Updated plugin version metadata, API User-Agent, and release documentation to `0.0.5`.

## [0.0.4] - 2026-10-15

### Added

- Multi-array PV configuration using slash-separated panel tilt, compass azimuth, panel count, and per-panel wattage.
- Independent forecast.solar request for each panel group, with period and daily energy summed by timestamp.
- Automatic total peak-power calculation from panel counts and rated wattage.
- Backward-compatible support for existing single-array configuration.

### Changed

- Multi-array azimuths use standard compass bearings (0° north, 90° east, 180° south, 270° west) and are converted internally to forecast.solar azimuth convention.
- Updated package metadata and documentation to version 0.0.4.

All notable user-facing changes for this project are documented here. This project uses a simple Keep a Changelog-inspired structure.

## [0.0.3] - 2026-10-14

### Added

- Added the `Next Hour Forecast` kWh sensor (Domoticz unit 4).
- The sensor estimates energy for the next complete clock-hour block, not a rolling 60-minute window. For example, at 17:44 it forecasts 18:00–19:00.
- Added fixed-time unit tests for next-hour boundary behavior.

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
- HTTP timeout/error handling and offline unit tests.
- Community documentation, contribution guidance, security policy, support guide, issue templates, and automated test workflow.

### Notes

- Forecasts are estimates and are not actual meter readings or financial earnings.
- Live Domoticz integration should be validated on a test instance before production use.
