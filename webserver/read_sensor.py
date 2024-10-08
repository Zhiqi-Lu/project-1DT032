from flask import Flask, jsonify, render_template_string
from sense_hat import SenseHat
import time
from threading import Thread

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

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plant Condition Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #d6f9d5;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            display: flex;
            justify-content: space-between;
            width: 80%;
            margin: 20px;
        }
        .left {
            width: 40%;
        }
        .right {
            width: 55%;
        }
        .condition-block {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 2.5rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .charts-section {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .chart-container {
            width: 100%;
            max-width: 600px;
            margin: 20px auto;
        }
        canvas {
            width: 100%;
            height: 400px;
        }
    </style>
</head>
<body>
    <h1>Plant Condition Dashboard</h1>
    <div class="container">
        <!-- Left Column for Plant Conditions -->
        <div class="left">
            <div class="condition-block">
                <h2 id="time"></h2>
                <p id="date"></p>
                <p id="temperature">Temperature: --°C</p>
                <p id="humidity">Humidity: --%</p>
                <p id="intensity">Pressure: -- lx</p>
            </div>
        </div>
        
        <!-- Right Column for Charts -->
        <div class="right">
            <section class="charts-section">
                <div class="chart-container">
                    <h3>Temperature</h3>
                    <canvas id="temperatureChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Humidity</h3>
                    <canvas id="humidityChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Light Intensity</h3>
                    <canvas id="PressureChart"></canvas>
                </div>
            </section>
        </div>
    </div>

    <script>
        // Fetch the current sensor data and update the UI
        function fetchCurrentSensorData() {
            fetch('/sensor')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('temperature').textContent = 'Temperature: ' + data.temperature + '°C';
                    document.getElementById('humidity').textContent = 'Humidity: ' + data.humidity + '%';
                    document.getElementById('intensity').textContent = 'Pressure: ' + data.intensity + ' lx';
                })
                .catch(error => console.error('Error fetching current sensor data:', error));
        }

        // Fetch the last 12 hours of sensor data and display in charts
        function fetchSensorHistory() {
            fetch('/sensor/history')
                .then(response => response.json())
                .then(data => {
                    const labels = data.map(item => {
                        const date = new Date(item.timestamp * 1000);
                        return `${date.getHours()}:${date.getMinutes()}`;
                    });

                    const temperatureData = data.map(item => item.temperature);
                    const humidityData = data.map(item => item.humidity);
                    const intensityData = data.map(item => item.intensity);

                    // Create charts
                    createChart('temperatureChart', labels, temperatureData, 'Temperature (°C)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 1)');
                    createChart('humidityChart', labels, humidityData, 'Humidity (%)', 'rgba(54, 162, 235, 0.2)', 'rgba(54, 162, 235, 1)');
                    createChart('PressureChart', labels, intensityData, 'Pressure (hPa)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 1)');
                })
                .catch(error => console.error('Error fetching sensor history:', error));
        }

        // Function to create a chart
        function createChart(elementId, labels, data, label, backgroundColor, borderColor) {
            const ctx = document.getElementById(elementId).getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: label,
                        data: data,
                        backgroundColor: backgroundColor,
                        borderColor: borderColor,
                        borderWidth: 1,
                        fill: true
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'category',
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: label
                            }
                        }
                    }
                }
            });
        }

        // Update time and date every second
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const dateString = now.toLocaleDateString([], { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
            document.getElementById('time').textContent = timeString;
            document.getElementById('date').textContent = dateString;
        }

        // Fetch sensor data and update every 5 minutes
        fetchCurrentSensorData();
        fetchSensorHistory();
        setInterval(fetchCurrentSensorData, 300000); // Refresh every 5 minutes
        setInterval(fetchSensorHistory, 300000);     // Refresh chart data every 5 minutes
        setInterval(updateTime, 1000);               // Update time every second
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    # Run the server and record data
    Thread(target=record_sensor_data).start()
    app.run(host='0.0.0.0', port=5000)

