"""Pure forecast parsing and calendar-boundary calculations."""
from datetime import datetime, time as datetime_time, timedelta


def parse_timestamp(value):
    """Parse forecast.solar timestamps into local-naive datetimes."""
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=None)


def parse_forecast(payload, now=None):
    """Return remaining energy today and tomorrow's daily energy in Wh.

    API period values are treated as interval energy beginning at each key.
    The current interval is prorated, and today's intervals are clipped at
    local midnight. This is a forecast estimate, not metered production.
    """
    if not isinstance(payload, dict):
        raise ValueError("API response is not a JSON object")
    message = payload.get("message") or {}
    if message.get("type") != "success":
        raise ValueError("{}: {}".format(message.get("type", "API error"), message.get("text", "no details")))
    result = payload.get("result") or {}
    periods_raw = result.get("watt_hours_period") or {}
    daily_raw = result.get("watt_hours_day") or {}
    if not isinstance(periods_raw, dict) or not isinstance(daily_raw, dict):
        raise ValueError("API response is missing forecast data")

    now = now or datetime.now()
    if now.tzinfo is not None:
        now = now.astimezone().replace(tzinfo=None)
    today = now.date()
    tomorrow = today + timedelta(days=1)
    midnight = datetime.combine(tomorrow, datetime_time.min)
    # "Next hour" means the next complete clock-hour block, not a rolling
    # 60-minute window. At 17:44, for example, this is 18:00-19:00.
    current_hour_start = now.replace(minute=0, second=0, microsecond=0)
    next_hour_start = current_hour_start if now == current_hour_start else current_hour_start + timedelta(hours=1)
    next_hour_end = next_hour_start + timedelta(hours=1)

    periods = []
    for timestamp, value in periods_raw.items():
        try:
            stamp, energy = parse_timestamp(timestamp), max(0.0, float(value))
        except (TypeError, ValueError, OverflowError):
            continue
        periods.append((stamp, energy))
    periods.sort(key=lambda item: item[0])
    if not periods:
        raise ValueError("API response contains no valid watt_hours_period entries")

    next_hour_energy = 0.0
    for index, (start, energy_wh) in enumerate(periods):
        # Period values are interval energy beginning at the timestamp. Use
        # the next timestamp as the interval end where available; otherwise
        # assume a one-hour interval. Only overlapping energy contributes.
        interval_end = periods[index + 1][0] if index + 1 < len(periods) else start + timedelta(hours=1)
        interval_end = min(interval_end, start + timedelta(hours=1))
        overlap_start = max(start, next_hour_start)
        overlap_end = min(interval_end, next_hour_end)
        if overlap_end > overlap_start:
            duration = (interval_end - start).total_seconds()
            if duration > 0:
                fraction = (overlap_end - overlap_start).total_seconds() / duration
                next_hour_energy += energy_wh * min(1.0, max(0.0, fraction))

    remaining = 0.0
    for index, (start, energy_wh) in enumerate(periods):
        if start.date() > today or start >= midnight:
            break
        end = periods[index + 1][0] if index + 1 < len(periods) else midnight
        end = min(end, midnight)
        if end <= start or end <= now:
            continue
        overlap_start = max(start, now)
        if end <= overlap_start:
            continue
        duration = (end - start).total_seconds()
        if duration > 0:
            fraction = (end - overlap_start).total_seconds() / duration
            remaining += energy_wh * min(1.0, max(0.0, fraction))

    daily = {}
    for timestamp, value in daily_raw.items():
        try:
            daily[parse_timestamp(timestamp).date()] = max(0.0, float(value))
        except (TypeError, ValueError, OverflowError):
            continue
    return {
        "today": today, "tomorrow": tomorrow,
        "remaining_today_wh": round(remaining),
        "tomorrow_wh": round(daily[tomorrow]) if tomorrow in daily else None,
        "next_hour_start": next_hour_start,
        "next_hour_end": next_hour_end,
        "next_hour_wh": round(next_hour_energy),
    }
