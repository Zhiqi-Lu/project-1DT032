// script.js

// Function to display current time with date
function updateTimeAndDate() {
    const dateContainer = document.getElementById('current-date');
    const timeContainer = document.getElementById('current-time');
    
    const now = new Date();
    
    // Date formatting
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Month is zero-based
    const day = String(now.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    
    // Time formatting
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    // const seconds = String(now.getSeconds()).padStart(2, '0');
    const formattedTime = `${hours}:${minutes}`;
    
    // Update the HTML elements
    dateContainer.textContent = formattedDate;
    timeContainer.textContent = formattedTime;
}

// Update time and date every second
setInterval(updateTimeAndDate, 1000);
/*
// Chart.js setup for each individual chart
const temperatureCtx = document.getElementById('temperatureChart').getContext('2d');
const humidityCtx = document.getElementById('humidityChart').getContext('2d');
const intensityCtx = document.getElementById('intensityChart').getContext('2d');

// Simulating data over 24 hours
const timeLabels = ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00'];
const temperatureData = [22, 23, 21, 24, 25, 26, 27, 28, 29, 26, 24, 23]; // Example data for temperature
const humidityData = [55, 60, 58, 62, 65, 68, 70, 72, 73, 71, 68, 64]; // Example data for humidity
const intensityData = [600, 750, 700, 850, 900, 950, 1100, 1200, 1150, 1000, 900, 750]; // Example data for light intensity

// Temperature chart
const temperatureChart = new Chart(temperatureCtx, {
    type: 'line',
    data: {
        labels: timeLabels,
        datasets: [{
            label: 'Temperature (°C)',
            data: temperatureData,
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true
            }
            //,
            //title: {
                //display: true,
                //text: 'Temperature (24 hours)'
            //}
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time of Day'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Temperature (°C)'
                }
            }
        }
    }
});

// Humidity chart
const humidityChart = new Chart(humidityCtx, {
    type: 'line',
    data: {
        labels: timeLabels,
        datasets: [{
            label: 'Humidity (%)',
            data: humidityData,
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true
            }
            //,
            //title: {
                //display: true,
                //text: 'Humidity (24 hours)'
            //}
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time of Day'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Humidity (%)'
                }
            }
        }
    }
});

// Light Intensity chart
const intensityChart = new Chart(intensityCtx, {
    type: 'line',
    data: {
        labels: timeLabels,
        datasets: [{
            label: 'Light Intensity (lx)',
            data: intensityData,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true
            }
            //,
            //title: {
             //   display: true,
              //  text: 'Light Intensity (24 hours)'
            //}
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time of Day'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Light Intensity (lx)'
                }
            }
        }
    }
});*/

// Fetch the last 12 hours of sensor data and display in a chart
function fetchSensorHistory() {
    fetch('http://<raspberry-pi-ip>:5000/sensor/history')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => {
                const date = new Date(item.timestamp * 1000);
                return `${date.getHours()}:${date.getMinutes()}`;
            });

            const temperatureData = data.map(item => item.temperature);
            const humidityData = data.map(item => item.humidity);
            const intensityData = data.map(item => item.intensity);

            // Create chart for temperature
            createChart('temperatureChart', labels, temperatureData, 'Temperature (°C)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 1)');
            // Create chart for humidity
            createChart('humidityChart', labels, humidityData, 'Humidity (%)', 'rgba(54, 162, 235, 0.2)', 'rgba(54, 162, 235, 1)');
            // Create chart for light intensity
            createChart('intensityChart', labels, intensityData, 'Light Intensity (lx)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 1)');
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

// Fetch and display history on page load
fetchSensorHistory();

// Function to fetch live sensor data
function fetchSensorData() {
    fetch('http://<raspberry-pi-ip>:5000/sensor')
        .then(response => response.json())
        .then(data => {
            const { temperature, humidity, pressure, intensity } = data;

            // Update the temperature, humidity, and intensity on the dashboard
            document.getElementById('temperature').innerText = `${temperature}°C`;
            document.getElementById('humidity').innerText = `${humidity}%`;
            document.getElementById('pressure').innerText = `${pressure}%`;
            document.getElementById('intensity').innerText = `${intensity} lx`;

            // Update background color based on temperature
            updateTemperatureAndBackground(temperature);
        })
        .catch(error => console.error('Error fetching sensor data:', error));
}

// Fetch sensor data every 5 seconds
setInterval(fetchSensorData, 5000);

