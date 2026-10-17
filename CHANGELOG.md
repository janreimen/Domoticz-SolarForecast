# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows Semantic Versioning where applicable.

## [Unreleased]

### Planned for 0.0.5

The following items describe the development goals for the next release. They are not considered released until implemented, tested, and included in a release.

#### Added

- Forecast-history functionality to retain forecast values over time, subject to implementation and verification.
- Documentation for interpreting forecast history and distinguishing forecasts from actual PV production.
- Additional test coverage for forecast history, missing data, and time-boundary calculations.

#### Changed

- Improve forecast error handling and status reporting.
- Review forecast calculations around local midnight and complete clock-hour boundaries.
- Review configuration validation and error messages for single-array and multi-array installations.
- Update documentation to match the implemented configuration parameters, device definitions, and forecast calculations.

#### Fixed

- Address issues discovered during development and testing, once verified and documented.
- Verify correct reporting of the last successful update time after successful polling.
- Verify handling of missing or incomplete forecast data without presenting unavailable values as genuine zero forecasts.

#### Testing

- Run automated tests for configuration, devices, forecast calculations, and history functionality.
- Run Python compilation checks.
- Test the development branch on a non-production Domoticz instance before release.

## [0.0.4] - Unreleased date to verify

### Added

- Multi-array PV configuration support.
- Configuration for panel inclination, orientation, panel count, and rated power per array.
- Combined peak-power calculation for configured arrays.

### Changed

- Extend forecast configuration and calculations to support installations with multiple panel orientations.
- Update plugin configuration
