from flask import Flask, jsonify
from weather import WeatherMonitor

app = Flask(__name__)
weather_monitor = WeatherMonitor()

@app.route('/weather', methods=['GET'])
def get_weather():
    return jsonify(weather_monitor.get_latest_weather())

if __name__ == '__main__':
    weather_monitor.start_monitoring()
    app.run(debug=True, host='0.0.0.0', port=5000)
