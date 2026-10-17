# Release process

This document describes how to prepare a repeatable community release. The current packaged version is `0.0.5`.

## Pre-release checklist

- [ ] Review changes and attribution/license obligations.
- [ ] Update `CHANGELOG.md` with user-visible changes.
- [ ] Update the plugin XML version in `plugin.py` and `solarforecast/__init__.py` together.
- [ ] Update the API User-Agent in `solarforecast/api.py` if the version changes.
- [ ] Run `python3 -m unittest discover -s tests -v`.
- [ ] Run `python3 -m compileall -q plugin.py solarforecast`.
- [ ] Test install/upgrade and device behavior on a non-production Domoticz instance.
- [ ] Verify forecast.solar responses, API limits, time zone behavior, and midnight cutoff.
- [ ] Check the archive contains source, docs, templates, tests, and license, but no `.env`, bytecode, or local secrets.
- [ ] Create a Git tag matching the plugin version only after review and validation.

## Versioning

Use semantic versioning conventions where practical. Because this plugin is early-stage, `0.x` releases may still change behavior. A release version must match in the XML metadata, package metadata, User-Agent, README, changelog, and release archive name.

## Build a source archive

Run this from the parent directory of the project folder:

```sh
zip -r Domoticz-SolarForecast-0.0.5.zip Domoticz-SolarForecast-0.0.5 \
  -x '*/.env' '*/__pycache__/*' '*.pyc' '*/.git/*' '*/.venv/*'
unzip -t Domoticz-SolarForecast-0.0.5.zip
unzip -l Domoticz-SolarForecast-0.0.5.zip
```

Run tests before packaging and verify that the archive's top-level folder and version match the release.
