
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Freezing fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Severe thunderstorm with hail",
}


def get_weather(city: str, day: str = "today"):
    """
    Get current weather or today's/tomorrow's forecast.
    day must be 'today' or 'tomorrow'.
    """
    try:
        day = day.lower().strip()

        if day not in ("today", "tomorrow"):
            return {"error": "Only today and tomorrow are supported."}

        # Convert a city name into geographical coordinates.
        location_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en"},
            timeout=10
        )
        location_response.raise_for_status()
        locations = location_response.json().get("results", [])

        if not locations:
            return {"error": f"Could not find city: {city}"}

        location = locations[0]

        # Request weather for the selected coordinates.
        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,weather_code,"
                    "wind_speed_10m"
                ),
                "daily": (
                    "temperature_2m_max,temperature_2m_min,"
                    "precipitation_probability_max,weather_code"
                ),
                "timezone": "auto",
                "forecast_days": 2
            },
            timeout=10
        )
        weather_response.raise_for_status()
        data = weather_response.json()

        index = 0 if day == "today" else 1
        daily = data["daily"]

        result = {
            "city": location["name"],
            "country": location.get("country"),
            "date": daily["time"][index],
            "forecast": WEATHER_CODES.get(
                daily["weather_code"][index], "Unknown"
            ),
            "high_c": daily["temperature_2m_max"][index],
            "low_c": daily["temperature_2m_min"][index],
            "rain_probability_percent": (
                daily["precipitation_probability_max"][index]
            ),
            "source": "Open-Meteo"
        }

        if day == "today":
            current = data["current"]
            result["current"] = {
                "temperature_c": current["temperature_2m"],
                "feels_like_c": current["apparent_temperature"],
                "humidity_percent": current["relative_humidity_2m"],
                "wind_kmh": current["wind_speed_10m"],
                "condition": WEATHER_CODES.get(
                    current["weather_code"], "Unknown"
                ),
                "observed_at": current["time"]
            }

        return result

    except requests.RequestException as error:
        return {"error": f"Weather service unavailable: {error}"}
    except (KeyError, ValueError, IndexError) as error:
        return {"error": f"Invalid weather response: {error}"}
