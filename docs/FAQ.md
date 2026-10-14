# Frequently Asked Questions

## Is Remaining Today actual production?

No. It is an estimate of PV energy expected from the current time until midnight. Use a production meter or inverter integration for actual generation.

## Is Tomorrow Forecast a cumulative energy counter?

No. It is a daily forecast value for tomorrow. Do not add it to actual meter readings or treat it as a monotonically increasing counter.

## Does the plugin report solar radiation?

Not in this release. The forecast.solar endpoint used here reports predicted PV power/energy, not a measured or forecast irradiance value in W/m². Irradiance must not be inferred by relabeling PV output.

## Why are there separate sensors for today and tomorrow?

They have different date windows. Remaining Today stops at local midnight; Tomorrow Forecast is the API's daily estimate for the next calendar day. Keeping them separate prevents double-counting across the day boundary.

## Can I use the forecast to calculate money earned?

This release does not estimate financial earnings. A meaningful calculation would need your tariff, export compensation, self-consumption assumptions, and the forecast energy period. Do not label kWh as currency.

## Why does a forecast change after a refresh?

Weather forecasts and provider estimates are updated over time. Changes are expected and do not necessarily indicate a plugin defect.

## Can I use several panel orientations?

The current configuration represents one panel plane/orientation. For materially different orientations, confirm provider capabilities and model each plane separately or add explicit multi-plane support in a future release. Do not simply combine orientations into a single azimuth.

## Does a passing test suite mean it works in Domoticz?

No. Unit tests verify offline calculations and configuration behavior. A live integration test against the intended Domoticz version is still required before production use.
