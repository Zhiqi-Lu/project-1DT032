// Fetch the current sensor data and update the UI
function fetchCurrentSensorData() {
    fetch('/sensor')
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperature').textContent = 'Temperature: ' + data.temperature + '°C';
            document.getElementById('humidity').textContent = 'Humidity: ' + data.humidity + '%';
            document.getElementById('intensity').textContent = 'Pressure: ' + data.intensity + 'hPa';
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