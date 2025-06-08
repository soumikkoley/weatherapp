from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'].title(),
                    'humidity': data['main']['humidity'],
                    'wind': data['wind']['speed']
                }
            else:
                error = "City not found"
        else:
            error = "Please enter a city name"

    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
