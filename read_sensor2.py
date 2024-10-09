import json
import time
from threading import Thread
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Store data for the last 12 hours (5-minute intervals = 144 data points)
data_history = []
json_file_path = 'sensor_data.json'

def get_sensor_data():
    # Simulated sensor data for testing
    return {
        'temperature': 10.11,
        'humidity': 20.22,
        'intensity': 1069,  # Assuming pressure as intensity
        'timestamp': time.time()
    }

def save_to_json(data):
    # Save data to JSON file (append mode)
    with open(json_file_path, 'a+') as f:
        f.seek(0)
        try:
            current_data = json.load(f)
        except json.JSONDecodeError:
            current_data = []
        current_data.append(data)
        f.seek(0)
        f.truncate()
        json.dump(current_data, f, indent=4)

def read_last_12_hours():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            try:
                current_data = json.load(f)
            except json.JSONDecodeError:
                return []

        # Filter data for the last 12 hours (43200 seconds)
        cutoff_time = time.time() - 43200
        last_12_hours_data = [entry for entry in current_data if entry['timestamp'] > cutoff_time]
        return last_12_hours_data
    else:
        return []

def record_sensor_data():
    global data_history
    data_history = read_last_12_hours()  # Load the last 12 hours of data

    while True:
        data = get_sensor_data()
        # Maintain only 144 data points (5-minute intervals for 12 hours)
        if len(data_history) >= 144:
            data_history.pop(0)  # Remove the oldest data point
        data_history.append(data)
        save_to_json(data)  # Save new data to JSON file
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
    Thread(target=record_sensor_data).start()
    app.run(host='0.0.0.0', port=5000)
