from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Replace with your API key if using OpenWeatherMap
API_KEY = "YOUR_API_KEY"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Weather REST API is running",
        "endpoint": "/api/weather?city=Pune"
    })


@app.route("/api/weather", methods=["GET"])
def get_weather():

    city = request.args.get("city")

    if not city:
        return jsonify({
            "error": "City parameter is required"
        }), 400

    if API_KEY == "YOUR_API_KEY":
        return jsonify({
            "error": "Please configure your weather API key"
        }), 500

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        data = response.json()

        if response.status_code != 200:
            return jsonify({
                "error": data.get(
                    "message",
                    "Unable to fetch weather data"
                )
            }), response.status_code

        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }

        return jsonify(weather), 200

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Weather service is currently unavailable"
        }), 503


if __name__ == "__main__":
    app.run(debug=True)