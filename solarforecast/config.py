"""Configuration loading and validation."""
import os

DEFAULTS = {
    "LATITUDE": "", "LONGITUDE": "", "PANEL_DECLINATION": "45",
    "PANEL_AZIMUTH": "0", "PANEL_PEAK_POWER_KWP": "4.8",
    "PANEL_AMOUNT": "", "PANEL_UNIQUE_POWER": "", "API_KEY": "",
    "POLL_INTERVAL_MINUTES": "10", "LOG_LEVEL": "INFO", "HTTP_TIMEOUT_SECONDS": "20",
}


def load_env_file(path):
    """Read KEY=VALUE settings without requiring python-dotenv."""
    values = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return values
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key:
            values[key] = value
    return values


def _number_list(value, name):
    try:
        result = [float(part.strip()) for part in str(value).split("/")]
    except (TypeError, ValueError):
        raise ValueError("{} must contain slash-separated numbers".format(name))
    if not result or any(not __import__("math").isfinite(item) for item in result):
        raise ValueError("{} must contain finite numbers".format(name))
    return result


def parse_config(env_values, domoticz_settings=None, process_env=None):
    """Merge defaults, .env and process environment, then validate values.

    Multi-array mode uses compass azimuths (0=N, 90=E, 180=S, 270=W).
    Legacy single-array mode retains forecast.solar's azimuth convention.
    """
    config = dict(DEFAULTS)
    config.update({k: v for k, v in env_values.items() if k in DEFAULTS})
    process_env = os.environ if process_env is None else process_env
    for key in DEFAULTS:
        if key in process_env:
            config[key] = process_env[key]

    if not config["LATITUDE"] and domoticz_settings:
        parts = str(domoticz_settings.get("Location", "")).split(";")
        if len(parts) >= 2:
            config["LATITUDE"], config["LONGITUDE"] = parts[0], parts[1]

    try:
        config["LATITUDE"] = float(config["LATITUDE"])
        config["LONGITUDE"] = float(config["LONGITUDE"])
        config["POLL_INTERVAL_MINUTES"] = int(config["POLL_INTERVAL_MINUTES"])
        config["HTTP_TIMEOUT_SECONDS"] = int(config["HTTP_TIMEOUT_SECONDS"])
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid numeric setting in .env: {}".format(exc))

    if not -90 <= config["LATITUDE"] <= 90:
        raise ValueError("LATITUDE must be between -90 and 90")
    if not -180 <= config["LONGITUDE"] <= 180:
        raise ValueError("LONGITUDE must be between -180 and 180")
    if config["POLL_INTERVAL_MINUTES"] < 5:
        raise ValueError("POLL_INTERVAL_MINUTES must be at least 5")
    if config["HTTP_TIMEOUT_SECONDS"] < 1:
        raise ValueError("HTTP_TIMEOUT_SECONDS must be positive")

    amount_value = str(config["PANEL_AMOUNT"]).strip()
    power_value = str(config["PANEL_UNIQUE_POWER"]).strip()
    multi_mode = bool(amount_value or power_value or "/" in str(config["PANEL_DECLINATION"]) or "/" in str(config["PANEL_AZIMUTH"]))
    if multi_mode:
        if not amount_value or not power_value:
            raise ValueError("Multi-array mode requires both PANEL_AMOUNT and PANEL_UNIQUE_POWER")
        tilts = _number_list(config["PANEL_DECLINATION"], "PANEL_DECLINATION")
        compass_azimuths = _number_list(config["PANEL_AZIMUTH"], "PANEL_AZIMUTH")
        amounts = _number_list(amount_value, "PANEL_AMOUNT")
        powers = _number_list(power_value, "PANEL_UNIQUE_POWER")
        lengths = {len(tilts), len(compass_azimuths), len(amounts), len(powers)}
        if len(lengths) != 1:
            raise ValueError("PANEL_DECLINATION, PANEL_AZIMUTH, PANEL_AMOUNT and PANEL_UNIQUE_POWER must have the same number of slash-separated entries")
        arrays = []
        for index, (tilt, compass, amount, watts) in enumerate(zip(tilts, compass_azimuths, amounts, powers), 1):
            if not 0 <= tilt <= 90:
                raise ValueError("PANEL_DECLINATION entry {} must be between 0 and 90".format(index))
            if not 0 <= compass <= 360:
                raise ValueError("PANEL_AZIMUTH entry {} must be a compass bearing between 0 and 360".format(index))
            if amount <= 0 or watts <= 0:
                raise ValueError("PANEL_AMOUNT and PANEL_UNIQUE_POWER entries must be greater than zero")
            # forecast.solar uses 0=south, -90=east, +90=west.
            api_azimuth = ((compass - 180 + 180) % 360) - 180
            kwp = amount * watts / 1000.0
            arrays.append({"declination": tilt, "azimuth": api_azimuth, "amount": int(amount) if amount.is_integer() else amount,
                           "unique_power_w": watts, "peak_power_kwp": kwp})
        config["PANEL_ARRAYS"] = arrays
        config["PANEL_PEAK_POWER_KWP"] = sum(item["peak_power_kwp"] for item in arrays)
        config["MULTI_ARRAY_MODE"] = True
    else:
        try:
            config["PANEL_DECLINATION"] = float(config["PANEL_DECLINATION"])
            config["PANEL_AZIMUTH"] = float(config["PANEL_AZIMUTH"])
            config["PANEL_PEAK_POWER_KWP"] = float(config["PANEL_PEAK_POWER_KWP"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Invalid numeric panel setting in .env: {}".format(exc))
        if not 0 <= config["PANEL_DECLINATION"] <= 90:
            raise ValueError("PANEL_DECLINATION must be between 0 and 90")
        if not -180 <= config["PANEL_AZIMUTH"] <= 180:
            raise ValueError("PANEL_AZIMUTH must be between -180 and 180 in legacy single-array mode")
        if config["PANEL_PEAK_POWER_KWP"] <= 0:
            raise ValueError("PANEL_PEAK_POWER_KWP must be greater than zero")
        config["PANEL_ARRAYS"] = [{"declination": config["PANEL_DECLINATION"], "azimuth": config["PANEL_AZIMUTH"],
                                  "peak_power_kwp": config["PANEL_PEAK_POWER_KWP"]}]
        config["MULTI_ARRAY_MODE"] = False

    config["LOG_LEVEL"] = str(config["LOG_LEVEL"]).upper()
    if config["LOG_LEVEL"] not in ("ERROR", "WARNING", "INFO", "DEBUG", "TRACE"):
        raise ValueError("LOG_LEVEL must be ERROR, WARNING, INFO, DEBUG, or TRACE")
    return config
