# read_sensor.py

from sense_hat import SenseHat
from flask import Flask, jsonify

app = Flask(__name__)
sense = SenseHat()

@app.route('/sensor')
def get_sensor_data():
    # Read sensor data
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    intensity = sense.get_pressure()  # Assuming this represents light intensity in some form

    # Return sensor data as JSON
    return jsonify({
        'temperature': round(temperature, 2),
        'humidity': round(humidity, 2),
        'intensity': round(intensity, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
