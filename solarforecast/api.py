"""HTTP client for the forecast.solar API."""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

USER_AGENT = "Domoticz-SolarForecast/0.0.4"


def build_forecast_url(config, array=None):
    """Build one array's URL. Never log it: an API key may be part of the path."""
    base = "https://api.forecast.solar"
    api_key = config.get("API_KEY", "").strip()
    if api_key:
        base += "/" + quote(api_key, safe="")
    array = array or config["PANEL_ARRAYS"][0]
    return "{}/estimate/{}/{}/{}/{}/{}".format(
        base, config["LATITUDE"], config["LONGITUDE"], array["declination"],
        array["azimuth"], array["peak_power_kwp"])


def _fetch_one(config, array, opener):
    request = Request(build_forecast_url(config, array), headers={
        "Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with opener(request, timeout=config["HTTP_TIMEOUT_SECONDS"]) as response:
            body = response.read().decode("utf-8")
        payload = json.loads(body)
    except HTTPError as exc:
        raise RuntimeError("forecast.solar returned HTTP {}".format(exc.code))
    except URLError as exc:
        raise RuntimeError("forecast.solar connection failed: {}".format(exc.reason))
    except json.JSONDecodeError:
        raise RuntimeError("forecast.solar returned invalid JSON")
    if not isinstance(payload, dict) or (payload.get("message") or {}).get("type") != "success":
        message = payload.get("message") or {} if isinstance(payload, dict) else {}
        raise RuntimeError("forecast.solar API error: {}".format(message.get("text", message.get("type", "invalid response"))))
    return payload


def fetch_forecast(config, opener=urlopen):
    """Fetch every configured array and sum matching period/day energy values."""
    arrays = config.get("PANEL_ARRAYS") or [{
        "declination": config["PANEL_DECLINATION"],
        "azimuth": config["PANEL_AZIMUTH"],
        "peak_power_kwp": config["PANEL_PEAK_POWER_KWP"],
    }]
    combined = {"message": {"type": "success", "text": "Combined forecast for {} PV array(s)".format(len(arrays))},
                "result": {"watt_hours_period": {}, "watt_hours_day": {}}}
    for array in arrays:
        payload = _fetch_one(config, array, opener)
        result = payload.get("result") or {}
        for field in ("watt_hours_period", "watt_hours_day"):
            values = result.get(field) or {}
            if not isinstance(values, dict):
                raise RuntimeError("forecast.solar response has invalid {} data".format(field))
            target = combined["result"][field]
            for timestamp, value in values.items():
                try:
                    target[timestamp] = target.get(timestamp, 0.0) + max(0.0, float(value))
                except (TypeError, ValueError, OverflowError):
                    continue
    return combined
