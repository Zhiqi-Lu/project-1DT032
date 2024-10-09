from flask import Flask, jsonify, render_template_string, render_template, request
# from sense_hat import SenseHat
import time
from threading import Thread

app = Flask(__name__)
# sense = SenseHat()

# Store data for the last 12 hours (5-minute intervals = 144 data points)
data_history = []
desired_min_temp = -1.0
desired_max_temp = -1.0
desired_min_humi = -1.0
desired_max_humi = -1.0

def get_sensor_data():
    return {
        'temperature': 10.11,
        'humidity': 20.22,
        'intensity': 1069,  # Assuming pressure as intensity
        'timestamp': time.time()
    }
    # return {
    #     'temperature': round(sense.get_temperature(), 2),
    #     'humidity': round(sense.get_humidity(), 2),
    #     'intensity': round(sense.get_pressure(), 2),  # Assuming pressure as intensity
    #     'timestamp': time.time()
    # }

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
        desired_min_temp = float(request.form.get('minTemp'))
        return jsonify({'message': 'desire min temp received successful'})
    elif 'maxTemp' in request.form:
        desired_max_temp = float(request.form.get('maxTemp'))
        return jsonify({'message': 'desire max temp received successful'})
    elif 'minHumi' in request.form:
        desired_min_humi = float(request.form.get('minHumi'))
        return jsonify({'message': 'desire min humi received successful'})
    else:
        desired_max_humi = float(request.form.get('maxHumi'))
        return jsonify({'message': 'desire max humi received successful'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Run the server and record data
    Thread(target=record_sensor_data).start()
    app.run(host='0.0.0.0', port=5000)

