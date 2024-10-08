from sense_hat import SenseHat
from flask import Flask, jsonify
import time

app = Flask(__name__)
sense = SenseHat()

# Store data for the last 12 hours (5-minute intervals = 144 data points)
data_history = []

def get_sensor_data():
    return {
        'temperature': round(sense.get_temperature(), 2),
        'humidity': round(sense.get_humidity(), 2),
        'intensity': round(sense.get_pressure(), 2),  # Assuming pressure as intensity
        'timestamp': time.time()
    }

# Function to record data every 5 minutes
def record_sensor_data():
    while True:
        data = get_sensor_data()
        # Maintain only 144 data points (5-minute intervals for 12 hours)
        if len(data_history) >= 144:
            data_history.pop(0)  # Remove the oldest data point
        data_history.append(data)
        time.sleep(300)  # Sleep for 5 minutes

@app.route('/sensor')
def get_current_sensor_data():
    # Return the most recent sensor data
    return jsonify(get_sensor_data())

@app.route('/sensor/history')
def get_sensor_history():
    # Return the last 12 hours of sensor data
    return jsonify(data_history)

if __name__ == '__main__':
    # Run the server and record data
    from threading import Thread
    Thread(target=record_sensor_data).start()
    app.run(host='0.0.0.0', port=5000)

