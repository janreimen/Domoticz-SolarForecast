# Frequently Asked Questions

## Is Remaining Today actual production?

No. Unit 6 is the forecast remainder for today, derived as Remaining Until Tomorrow 23:59 (unit 1) minus Forecast Tomorrow (unit 2). It is not measured production. Unit 1 covers the current remainder plus tomorrow's forecast.

## Is Forecast Tomorrow a cumulative energy counter?

No. It is a daily forecast value for tomorrow. Do not add it to actual meter readings or treat it as a monotonically increasing counter.

## What time period does Next Full Hour cover?

It covers the next complete clock-hour block, not the next 60 minutes from the current instant. For example, at 17:44 it covers 18:00–19:00. The value is forecast energy in kWh, not instantaneous power.

## Does the plugin report solar radiation?

Not in this release. The forecast.solar endpoint used here reports predicted PV power/energy, not a measured or forecast irradiance value in W/m². Irradiance must not be inferred by relabeling PV output.

## Why are there separate sensors for today and tomorrow?

Unit 1 covers the remainder of today and all of tomorrow. Unit 2 is tomorrow's daily estimate. Unit 6 is calculated as unit 1 minus unit 2, so you can also see today's remainder separately.

## Can I use the forecast to calculate money earned?

This release does not estimate financial earnings. A meaningful calculation would need your tariff, export compensation, self-consumption assumptions, and the forecast energy period. Do not label kWh as currency.

## Why does a forecast change after a refresh?

Weather forecasts and provider estimates are updated over time. Changes are expected and do not necessarily indicate a plugin defect.

## Can I use several panel orientations?

Yes. Version 0.0.4 and later support slash-separated values for panel declination, compass azimuth, panel count, and per-panel wattage. All four lists must have the same number of entries. See the configuration guide for examples.

## Does a passing test suite mean it works in Domoticz?

No. Unit tests verify offline calculations and configuration behavior. A live integration test against the intended Domoticz version is still required before production use.

## Is the cumulative counter electricity usage?

No. Unit 5 is configured as generated/returned energy (`Switchtype=4`) because it accumulates predicted solar energy. Its cumulative total is forecast history, not measured generation or household consumption.
