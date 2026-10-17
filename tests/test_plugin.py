import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from solarforecast.api import build_forecast_url, fetch_forecast
from solarforecast.config import parse_config
from solarforecast.forecast import parse_forecast


class ConfigTests(unittest.TestCase):
    def test_valid_config(self):
        config = parse_config(
            {
                "LATITUDE": "49.6",
                "LONGITUDE": "6.1",
                "PANEL_DECLINATION": "30",
                "PANEL_AZIMUTH": "10",
                "PANEL_PEAK_POWER_KWP": "7.2",
                "POLL_INTERVAL_MINUTES": "15",
                "LOG_LEVEL": "DEBUG",
            },
            process_env={},
        )

        self.assertEqual(config["LATITUDE"], 49.6)
        self.assertEqual(config["POLL_INTERVAL_MINUTES"], 15)
        self.assertEqual(config["LOG_LEVEL"], "DEBUG")

    def test_domoticz_location_with_altitude(self):
        config = parse_config(
            {},
            {"Location": "49.6;6.1;300"},
            process_env={},
        )

        self.assertEqual(config["LATITUDE"], 49.6)
        self.assertEqual(config["LONGITUDE"], 6.1)

    def test_multi_array_configuration_and_total_peak_power(self):
        config = parse_config(
            {
                "LATITUDE": "49.71",
                "LONGITUDE": "6.25",
                "PANEL_DECLINATION": "30/45/30",
                "PANEL_AZIMUTH": "180/90/270",
                "PANEL_AMOUNT": "22/5/5",
                "PANEL_UNIQUE_POWER": "310/305/480",
                "PANEL_PEAK_POWER_KWP": "",
            },
            process_env={},
        )

        self.assertTrue(config["MULTI_ARRAY_MODE"])
        self.assertEqual(len(config["PANEL_ARRAYS"]), 3)
        self.assertAlmostEqual(config["PANEL_PEAK_POWER_KWP"], 10.745)
        self.assertEqual(
            [array["azimuth"] for array in config["PANEL_ARRAYS"]],
            [0.0, -90.0, 90.0],
        )
        self.assertEqual(
            [array["peak_power_kwp"] for array in config["PANEL_ARRAYS"]],
            [6.82, 1.525, 2.4],
        )

    def test_multi_array_lengths_must_match(self):
        with self.assertRaisesRegex(ValueError, "same number"):
            parse_config(
                {
                    "LATITUDE": "49",
                    "LONGITUDE": "6",
                    "PANEL_DECLINATION": "30/45",
                    "PANEL_AZIMUTH": "180/90/270",
                    "PANEL_AMOUNT": "22/5/5",
                    "PANEL_UNIQUE_POWER": "310/305/480",
                },
                process_env={},
            )

    def test_invalid_interval(self):
        with self.assertRaises(ValueError):
            parse_config(
                {
                    "LATITUDE": "49",
                    "LONGITUDE": "6",
                    "POLL_INTERVAL_MINUTES": "1",
                },
                process_env={},
            )

    def test_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            parse_config(
                {"LATITUDE": "91", "LONGITUDE": "6"},
                process_env={},
            )


class ForecastTests(unittest.TestCase):
    def setUp(self):
        self.base = {
            "message": {"type": "success", "text": "ok"},
            "result": {},
        }

    def test_api_key_is_url_encoded(self):
        config = parse_config(
            {
                "LATITUDE": "49.6",
                "LONGITUDE": "6.1",
                "API_KEY": "secret/key",
                "PANEL_DECLINATION": "30",
                "PANEL_AZIMUTH": "0",
                "PANEL_PEAK_POWER_KWP": "5",
            },
            process_env={},
        )

        url = build_forecast_url(config)

        self.assertIn("/secret%2Fkey/estimate/", url)
        self.assertNotIn("None", url)

    def test_multi_array_forecasts_are_summed(self):
        config = parse_config(
            {
                "LATITUDE": "49.71",
                "LONGITUDE": "6.25",
                "PANEL_DECLINATION": "30/45",
                "PANEL_AZIMUTH": "180/90",
                "PANEL_AMOUNT": "22/5",
                "PANEL_UNIQUE_POWER": "310/305",
                "PANEL_PEAK_POWER_KWP": "",
            },
            process_env={},
        )

        class Response:
            def __init__(self, body):
                self.body = body

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return self.body.encode("utf-8")

        bodies = [
            (
                '{"message":{"type":"success"},"result":'
                '{"watt_hours_period":{"2026-10-14 12:00:00":1000},'
                '"watt_hours_day":{"2026-10-15 00:00:00":5000}}}'
            ),
            (
                '{"message":{"type":"success"},"result":'
                '{"watt_hours_period":{"2026-10-14 12:00:00":250},'
                '"watt_hours_day":{"2026-10-15 00:00:00":1250}}}'
            ),
        ]

        calls = []

        def opener(request, timeout):
            calls.append(request.full_url)
            return Response(bodies[len(calls) - 1])

        result = fetch_forecast(config, opener=opener)

        self.assertEqual(len(calls), 2)
        self.assertEqual(
            result["result"]["watt_hours_period"]["2026-10-14 12:00:00"],
            1250,
        )
        self.assertEqual(
            result["result"]["watt_hours_day"]["2026-10-15 00:00:00"],
            6250,
        )

    def test_remaining_today_is_prorated_and_tomorrow_is_separate(self):
        payload = dict(self.base)
        payload["result"] = {
            "watt_hours_period": {
                "2026-10-14 10:00:00": 1000,
                "2026-10-14 11:00:00": 2000,
                "2026-10-14 12:00:00": 3000,
                "2026-10-14 23:00:00": 1000,
                "2026-10-15 00:00:00": 9000,
            },
            "watt_hours_day": {
                "2026-10-14 00:00:00": 12000,
                "2026-10-15 00:00:00": 5500,
            },
        }

        result = parse_forecast(
            payload,
            now=datetime(2026, 10, 14, 10, 30),
        )

        self.assertEqual(result["remaining_today_wh"], 6500)
        self.assertEqual(result["tomorrow_wh"], 5500)
        self.assertEqual(result["tomorrow"].isoformat(), "2026-10-15")

    def test_midnight_cutoff(self):
        payload = dict(self.base)
        payload["result"] = {
            "watt_hours_period": {
                "2026-10-14 23:00:00": 1000,
                "2026-10-15 00:00:00": 8000,
            },
            "watt_hours_day": {
                "2026-10-15 00:00:00": 5000,
            },
        }

        result = parse_forecast(
            payload,
            now=datetime(2026, 10, 14, 23, 30),
        )

        self.assertEqual(result["remaining_today_wh"], 500)
        self.assertEqual(result["tomorrow_wh"], 5000)

    def test_next_hour_is_next_complete_clock_hour(self):
        payload = dict(self.base)
        payload["result"] = {
            "watt_hours_period": {
                "2026-10-14 17:00:00": 1700,
                "2026-10-14 18:00:00": 1800,
                "2026-10-14 19:00:00": 1900,
                "2026-10-14 20:00:00": 2000,
            },
            "watt_hours_day": {
                "2026-10-15 00:00:00": 5500,
            },
        }

        result = parse_forecast(
            payload,
            now=datetime(2026, 10, 14, 17, 44),
        )

        self.assertEqual(
            result["next_hour_start"],
            datetime(2026, 10, 14, 18, 0),
        )
        self.assertEqual(
            result["next_hour_end"],
            datetime(2026, 10, 14, 19, 0),
        )
        self.assertEqual(result["next_hour_wh"], 1800)

    def test_at_exact_hour_uses_current_hour_block(self):
        payload = dict(self.base)
        payload["result"] = {
            "watt_hours_period": {
                "2026-10-14 17:00:00": 1700,
                "2026-10-14 18:00:00": 1800,
            },
            "watt_hours_day": {
                "2026-10-15 00:00:00": 5500,
            },
        }

        result = parse_forecast(
            payload,
            now=datetime(2026, 10, 14, 17, 0),
        )

        self.assertEqual(
            result["next_hour_start"],
            datetime(2026, 10, 14, 17, 0),
        )
        self.assertEqual(
            result["next_hour_end"],
            datetime(2026, 10, 14, 18, 0),
        )
        self.assertEqual(result["next_hour_wh"], 1700)

    def test_next_hour_rolls_over_midnight(self):
        payload = dict(self.base)
        payload["result"] = {
            "watt_hours_period": {
                "2026-10-14 23:00:00": 1000,
                "2026-10-15 00:00:00": 250,
                "2026-10-15 01:00:00": 500,
            },
            "watt_hours_day": {
                "2026-10-15 00:00:00": 5500,
            },
        }

        result = parse_forecast(
            payload,
            now=datetime(2026, 10, 14, 23, 45),
        )

        self.assertEqual(
            result["next_hour_start"],
            datetime(2026, 10, 15, 0, 0),
        )
        self.assertEqual(
            result["next_hour_end"],
            datetime(2026, 10, 15, 1, 0),
        )
        self.assertEqual(result["next_hour_wh"], 250)

    def test_api_error(self):
        with self.assertRaises(ValueError):
            parse_forecast(
                {
                    "message": {
                        "type": "warning",
                        "text": "rate limit",
                    },
                    "result": {},
                }
            )

    def test_no_period_data(self):
        with self.assertRaises(ValueError):
            parse_forecast(
                {
                    "message": {"type": "success"},
                    "result": {"watt_hours_day": {}},
                },
                now=datetime(2026, 10, 14, 12),
            )

    def test_missing_tomorrow_daily_forecast_is_explicit(self):
        payload = dict(self.base)
        payload["result"] = {
            "watt_hours_period": {
                "2026-10-14 23:00:00": 1000,
            },
            "watt_hours_day": {
                "2026-10-14 00:00:00": 1000,
            },
        }

        result = parse_forecast(
            payload,
            now=datetime(2026, 10, 14, 23, 30),
        )

        self.assertIsNone(result["tomorrow_wh"])


if __name__ == "__main__":
    unittest.main()
