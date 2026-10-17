"""Domoticz device declarations and safe update helpers."""

REMAINING_TODAY_UNIT = 1
TOMORROW_UNIT = 2
STATUS_UNIT = 3
NEXT_HOUR_UNIT = 4
FORECAST_ENERGY_COUNTER_UNIT = 5
REMAINING_TODAY_DETAIL_UNIT = 6

DEVICE_DEFINITIONS = (
    (REMAINING_TODAY_UNIT, "Forecast Remaining (Today + Tomorrow)", "Custom", {"Custom": "1;kWh"}),
    (TOMORROW_UNIT, "Forecast Tomorrow", "Custom", {"Custom": "1;kWh"}),
    (STATUS_UNIT, "Forecast Status", "Text", {}),
    (NEXT_HOUR_UNIT, "Forecast Next Full Hour", "Custom", {"Custom": "1;kWh"}),
    # Native Domoticz electricity-generation meter: sValue is "power_w;total_energy_wh".
    (FORECAST_ENERGY_COUNTER_UNIT, "Cumulative Forecast Energy", "kWh",
     {"AddDBLogEntry": "true"}),
    (REMAINING_TODAY_DETAIL_UNIT, "Forecast Remaining Today", "Custom", {"Custom": "1;kWh"}),
)


def ensure_devices(domoticz, devices):
    """Create only missing units; stable unit numbers preserve plugin identity."""
    for unit, name, type_name, options in DEVICE_DEFINITIONS:
        if unit not in devices:
            kwargs = {"Name": name, "Unit": unit, "TypeName": type_name,
                      "Options": options, "Used": 1}
            if unit == FORECAST_ENERGY_COUNTER_UNIT:
                kwargs["Switchtype"] = 4  # Electricity generated/returned, not electricity usage.
            domoticz.Device(**kwargs).Create()
            continue

        # Domoticz exposes Name and SwitchType as writable plugin-device properties.
        # Keep unit numbers/IDX identities stable while aligning existing labels.
        item = devices[unit]
        try:
            if getattr(item, "Name", name) != name:
                item.Name = name
        except (AttributeError, TypeError):
            pass
        if unit == FORECAST_ENERGY_COUNTER_UNIT:
            try:
                if getattr(item, "SwitchType", 4) != 4:
                    item.SwitchType = 4
            except (AttributeError, TypeError):
                pass


def update_unit(domoticz, devices, unit, value, log, force=False):
    """Update a unit safely; force=True also records unchanged samples."""
    item = devices.get(unit)
    if item is None:
        log("WARNING", "Domoticz unit {} is missing; it may have been deleted".format(unit))
        return
    value = str(value)
    # Domoticz exposes nValue and sValue as read-only properties on plugin
    # device objects. Values must be supplied to Update(), not assigned first.
    if force or getattr(item, "nValue", None) != 0 or getattr(item, "sValue", None) != value:
        item.Update(0, value)
