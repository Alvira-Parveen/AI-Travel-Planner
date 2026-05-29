import requests


def get_weather(latitude, longitude):
    """
    Fetch weather data using Open-Meteo API.
    """

    try:

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            f"&daily=temperature_2m_max,weathercode"
            f"&timezone=auto"
        )

        response = requests.get(url)

        weather_data = response.json()

        # Extract daily weather
        dates = weather_data["daily"]["time"]
        temperatures = weather_data["daily"]["temperature_2m_max"]

        formatted_weather = []

        for i in range(len(dates)):

            formatted_weather.append(
                f"""
Date: {dates[i]}
Max Temperature: {temperatures[i]}°C
-----------------------------------
"""
            )

        return "\n".join(formatted_weather)

    except Exception as e:
        return f"Error: {str(e)}"