# api: 7aa644cfacb844ccb00154420243008

# http://api.weatherapi.com/v1/forecast.json?key=7aa644cfacb844ccb00154420243008&q=London&days=5&aqi=no&alerts=no

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '7aa644cfacb844ccb00154420243008'
WEATHER_URL = 'http://api.weatherapi.com/v1/forecast.json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    params = {
        'key': API_KEY,
        'q': city,
        'days': 5,
        'aqi': 'no',
        'alerts': 'no'
    }
    response = requests.get(WEATHER_URL, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        today_hour_map = {}
        future_day_map = {}
        local_time = weather_data['location']['localtime']
        for hour in weather_data['forecast']['forecastday'][0]['hour']:
            if hour['time'] > local_time:    
                today_hour_map[hour['time']] = {
                    'temp_f': hour['temp_f'],
                    'weather': hour['condition']['text']
                }
        
        for days in weather_data['forecast']['forecastday'][1:5]:
            days['date'] = days['date']
            future_day_map[days['date']] = {
                'maxtemp_f': days['day']['maxtemp_f'],
                'mintemp_f': days['day']['mintemp_f'],
                'weather': days['day']['condition']['text']
            }

        weather_details = {
            'city': weather_data['location']['name'],
            'country': weather_data['location']['country'],
            'localtime': weather_data['location']['localtime'],
            'cur_temp_fahrenheit': weather_data['current']['temp_f'],
            'cur_weather': weather_data['current']['condition']['text'],
            'cur_maxtemp_fahrenheit': weather_data['forecast']['forecastday'][0]['day']['maxtemp_f'],
            'cur_mintemp_fahrenheit': weather_data['forecast']['forecastday'][0]['day']['mintemp_f'],
            'today_hour_map': today_hour_map,
            'future_day_map': future_day_map
        }
        return render_template('weather.html', weather=weather_details)
    else:
        error_message = weather_data.get('message', 'City not found!')
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
