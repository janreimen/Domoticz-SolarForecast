"""HTTP client for the forecast.solar API."""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

USER_AGENT = "Domoticz-SolarForecast/0.0.2"


def build_forecast_url(config):
    """Build the URL. Never log it: an API key may be part of the path."""
    base = "https://api.forecast.solar"
    api_key = config.get("API_KEY", "").strip()
    if api_key:
        base += "/" + quote(api_key, safe="")
    return "{}/estimate/{}/{}/{}/{}/{}".format(
        base, config["LATITUDE"], config["LONGITUDE"], config["PANEL_DECLINATION"],
        config["PANEL_AZIMUTH"], config["PANEL_PEAK_POWER_KWP"])


def fetch_forecast(config, opener=urlopen):
    """Fetch and decode a forecast, translating transport errors to RuntimeError."""
    request = Request(build_forecast_url(config), headers={
        "Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with opener(request, timeout=config["HTTP_TIMEOUT_SECONDS"]) as response:
            body = response.read().decode("utf-8")
        return json.loads(body)
    except HTTPError as exc:
        raise RuntimeError("forecast.solar returned HTTP {}".format(exc.code))
    except URLError as exc:
        raise RuntimeError("forecast.solar connection failed: {}".format(exc.reason))
    except json.JSONDecodeError:
        raise RuntimeError("forecast.solar returned invalid JSON")
