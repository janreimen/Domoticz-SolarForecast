"""Domoticz device declarations and safe update helpers."""

REMAINING_TODAY_UNIT = 1
TOMORROW_UNIT = 2
STATUS_UNIT = 3
NEXT_HOUR_UNIT = 4

DEVICE_DEFINITIONS = (
    (REMAINING_TODAY_UNIT, "Remaining Today", "Custom", {"Custom": "1;kWh"}),
    (TOMORROW_UNIT, "Tomorrow Forecast", "Custom", {"Custom": "1;kWh"}),
    (STATUS_UNIT, "Status", "Text", {}),
    (NEXT_HOUR_UNIT, "Next Hour Forecast", "Custom", {"Custom": "1;kWh"}),
)


def ensure_devices(domoticz, devices):
    """Create only missing units; stable unit numbers preserve plugin identity."""
    for unit, name, type_name, options in DEVICE_DEFINITIONS:
        if unit not in devices:
            domoticz.Device(Name=name, Unit=unit, TypeName=type_name,
                            Options=options, Used=1).Create()


def update_unit(domoticz, devices, unit, value, log):
    """Update only when the value changed; tolerate user-deleted devices."""
    item = devices.get(unit)
    if item is None:
        log("WARNING", "Domoticz unit {} is missing; it may have been deleted".format(unit))
        return
    value = str(value)
    # Domoticz exposes nValue and sValue as read-only properties on plugin
    # device objects. Values must be supplied to Update(), not assigned first.
    if getattr(item, "nValue", None) != 0 or getattr(item, "sValue", None) != value:
        item.Update(0, value)
