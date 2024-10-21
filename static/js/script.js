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

function fetchDesiredValue() {
    fetch('/desiredValue')
        .then(response => response.json())
        .then(data => {
            const minTemp = data.minTemp;
            const maxTemp = data.maxTemp;
            const minHumi = data.minHumi;
            const maxHumi = data.maxHumi;

            updateDesiredValue('minTemp', minTemp)
            updateDesiredValue('maxTemp', maxTemp)
            updateDesiredValue('minHumi', minHumi)
            updateDesiredValue('maxHumi', maxHumi)
        })
        .catch(error => console.error('Error fetching desired value:', error));
}

function fetchAlert() {
    fetch('/tolerance')
        .then(response => response.json())
        .then(data => {
            const tempAlert = data.tempAlert;
            const humiAlert = data.humiAlert;

            if (tempAlert && humiAlert) {
                window.alert("Temperature and Humidity are out of desired value range")
            }
            else if (tempAlert) {
                window.alert("Temperature is out of desired value range")
            }
            else if (humiAlert) {
                window.alert("Humidity is out of desired value range")
            }
        })
        .catch(error => console.error('Error fetching alert status:', error));
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

function updateDesiredValue(fieldName, desiredValue) {
    if (fieldName == 'minTemp') {
        if (desiredValue < 0 || desiredValue > 100) {
            document.getElementById('minTempSpan').textContent = "No desired minimum temperature"
        }
        else {
            document.getElementById('minTempSpan').textContent = "The current minimum desired temperature is:" + desiredValue
        }
    }
    else if (fieldName == 'maxTemp') {
        if (desiredValue < 0 || desiredValue > 100) {
            document.getElementById('maxTempSpan').textContent = "No desired maximum temperature"
        }
        else {
            document.getElementById('maxTempSpan').textContent = "The current maximum desired temperature is:" + desiredValue
        }
    }
    else if (fieldName == 'minHumi') {
        if (desiredValue < 0 || desiredValue > 100) {
            document.getElementById('minHumiSpan').textContent = "No desired minimum humidity"
        }
        else {
            document.getElementById('minHumiSpan').textContent = "The current minimum desired humidity is:" + desiredValue
        }
    }
    else {
        if (desiredValue < 0 || desiredValue > 100) {
            document.getElementById('maxHumiSpan').textContent = "No desired maximum humidity"
        }
        else {
            document.getElementById('maxHumiSpan').textContent = "The current maximum desired humidity is:" + desiredValue
        }
    }
}

//set desired value
async function handleFormSubmission(event, fieldName) {
    event.preventDefault();  // Prevent the default form submission

    const formData = new FormData();
    const desiredValue = document.getElementById(fieldName).value

    // Dynamically append the field based on the provided field name
    formData.append(fieldName, desiredValue);

    try {
        const response = await fetch(window.location.href + 'upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            console.log('desire value setting successful: ' + JSON.stringify(result));
            updateDesiredValue(fieldName, desiredValue)
        } else {
            const result = await response.json();
            alert(result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while setting desired value');
    }
}

// Fetch sensor data and update every 5 minutes
fetchCurrentSensorData();
fetchSensorHistory();
fetchDesiredValue();
setInterval(fetchCurrentSensorData, 60000); // Refresh every minute
setInterval(fetchAlert, 60000) // check backend whether there are any alert every minute
setInterval(fetchSensorHistory, 60000); // Refresh chart data every minute
setInterval(updateTime, 1000); // Update time every second
window.onload=function(){
    document.getElementById('uploadMinTemp').addEventListener('submit', function(event) {
        handleFormSubmission(event, 'minTemp');
    });
    document.getElementById('uploadMaxTemp').addEventListener('submit', function(event) {
        handleFormSubmission(event, 'maxTemp');
    });
    document.getElementById('uploadMinHumi').addEventListener('submit', function(event) {
        handleFormSubmission(event, 'minHumi');
    });
    document.getElementById('uploadMaxHumi').addEventListener('submit', function(event) {
        handleFormSubmission(event, 'maxHumi');
    });
}
