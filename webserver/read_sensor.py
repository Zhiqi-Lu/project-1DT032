import json
import os

from flask import Flask, jsonify, render_template_string, render_template, request
from sense_hat import SenseHat
import time
from threading import Thread

app = Flask(__name__)
sense = SenseHat()

# Store data for the last 12 hours (5-minute intervals = 144 data points)
data_history = []
desired_min_temp = -1.0
desired_max_temp = -1.0
desired_min_humi = -1.0
desired_max_humi = -1.0
json_file_path = 'sensor_data.json'

def get_sensor_data():
    return {
        'temperature': round(sense.get_temperature(), 2),
        'humidity': round(sense.get_humidity(), 2),
        'intensity': round(sense.get_pressure(), 2),  # Assuming pressure as intensity
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

# Function to record data every 5 minutes
def record_sensor_data():
    global data_history
    data_history = read_last_12_hours()  # Load the last 12 hours of data

    while True:
        data = get_sensor_data()
        # Maintain only 144 data points (5-minute intervals for 12 hours)
        if len(data_history) >= 720:
            data_history.pop(0)  # Remove the oldest data point
        data_history.append(data)
        save_to_json(data)
        time.sleep(60)  # Sleep for 5 minutes

@app.route('/sensor')
def get_current_sensor_data():
    # Return the most recent sensor data
    return jsonify(get_sensor_data())

@app.route('/sensor/history')
def get_sensor_history():
    # Return the last 12 hours of sensor data
    return jsonify(data_history)

@app.route('/tolerance')
def get_tolerance():
    global desired_min_temp
    global desired_max_temp
    global desired_min_humi
    global desired_max_humi

    temp_flag = False
    humi_flag = False
    env_data = get_sensor_data()
    if desired_min_temp >= 0 and env_data['temperature'] < desired_min_temp:
        temp_flag = True
    if 0 <= desired_max_temp <= 100 and env_data['temperature'] > desired_max_temp:
        temp_flag = True
    if desired_min_humi >= 0 and env_data['humidity'] < desired_min_humi:
        humi_flag = True
    if 0 <= desired_max_humi <= 100 and env_data['humidity'] > desired_max_humi:
        humi_flag = True
    return jsonify({'tempAlert': temp_flag, 'humiAlert': humi_flag})

@app.route('/desiredValue')
def get_desired_values():
    return jsonify({
        'minTemp': desired_min_temp,
        'maxTemp': desired_max_temp,
        'minHumi': desired_min_humi,
        'maxHumi': desired_max_humi})

@app.route('/upload', methods=['POST'])
def upload():
    global desired_min_temp
    global desired_max_temp
    global desired_min_humi
    global desired_max_humi

    if 'minTemp' in request.form:
        payload = float(request.form.get('minTemp'))
        if 0 < desired_max_temp < payload:
            return jsonify({'message': 'minimum desired temperature must be smaller than desired maximum temperature'}), 400
        desired_min_temp = payload
        return jsonify({'message': 'desire min temp received successful'})
    elif 'maxTemp' in request.form:
        payload = float(request.form.get('maxTemp'))
        if payload < desired_min_temp:
            return jsonify({'message': 'maximum desired temperature must be greater than desired minimum temperature'}), 400
        desired_max_temp = payload
        return jsonify({'message': 'desire max temp received successful'})
    elif 'minHumi' in request.form:
        payload = float(request.form.get('minHumi'))
        if 0 < desired_max_humi < payload:
            return jsonify({'message': 'minimum desired humidity must be smaller than desired maximum humidity'}), 400
        desired_min_humi = payload
        return jsonify({'message': 'desire min humi received successful'})
    else:
        payload = float(request.form.get('maxHumi'))
        if payload < desired_min_humi:
            return jsonify({'message': 'maximum desired humidity must be greater than desired maximum humidity'}), 400
        desired_max_humi = payload
        return jsonify({'message': 'desire max humi received successful'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Run the server and record data
    Thread(target=record_sensor_data).start()
    app.run(host='0.0.0.0', port=5000)

