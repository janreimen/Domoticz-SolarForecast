"""Configuration loading and validation."""
import os

DEFAULTS = {
    "LATITUDE": "", "LONGITUDE": "", "PANEL_DECLINATION": "45",
    "PANEL_AZIMUTH": "0", "PANEL_PEAK_POWER_KWP": "4.8", "API_KEY": "",
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


def parse_config(env_values, domoticz_settings=None, process_env=None):
    """Merge defaults, .env and process environment, then validate values."""
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
        for key in ("LATITUDE", "LONGITUDE", "PANEL_DECLINATION", "PANEL_AZIMUTH", "PANEL_PEAK_POWER_KWP"):
            config[key] = float(config[key])
        config["POLL_INTERVAL_MINUTES"] = int(config["POLL_INTERVAL_MINUTES"])
        config["HTTP_TIMEOUT_SECONDS"] = int(config["HTTP_TIMEOUT_SECONDS"])
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid numeric setting in .env: {}".format(exc))

    if not -90 <= config["LATITUDE"] <= 90:
        raise ValueError("LATITUDE must be between -90 and 90")
    if not -180 <= config["LONGITUDE"] <= 180:
        raise ValueError("LONGITUDE must be between -180 and 180")
    if not 0 <= config["PANEL_DECLINATION"] <= 90:
        raise ValueError("PANEL_DECLINATION must be between 0 and 90")
    if not -180 <= config["PANEL_AZIMUTH"] <= 180:
        raise ValueError("PANEL_AZIMUTH must be between -180 and 180")
    if config["PANEL_PEAK_POWER_KWP"] <= 0:
        raise ValueError("PANEL_PEAK_POWER_KWP must be greater than zero")
    if config["POLL_INTERVAL_MINUTES"] < 5:
        raise ValueError("POLL_INTERVAL_MINUTES must be at least 5")
    if config["HTTP_TIMEOUT_SECONDS"] < 1:
        raise ValueError("HTTP_TIMEOUT_SECONDS must be positive")
    config["LOG_LEVEL"] = str(config["LOG_LEVEL"]).upper()
    if config["LOG_LEVEL"] not in ("ERROR", "WARNING", "INFO", "DEBUG", "TRACE"):
        raise ValueError("LOG_LEVEL must be ERROR, WARNING, INFO, DEBUG, or TRACE")
    return config
