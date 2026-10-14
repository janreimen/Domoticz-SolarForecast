# Release process

This document describes how to prepare a repeatable community release. The current packaged version is `0.0.2`.

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

From the parent directory:

```sh
zip -r Domoticz-SolarForecast-0.0.2.zip Domoticz-SolarForecast-0.0.2 \
  -x '*/.env' '*/__pycache__/*' '*.pyc' '*/.git/*' '*/.venv/*'
```

Run tests before packaging and verify the resulting archive with `unzip -l`.
