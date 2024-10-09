import json
from sense_hat import SenseHat

class Sensor:
    def _init_(self):
        self.sensor = SenseHat()
        self.sensor.gain = 60
        self.sensor.integration_cycles = 256

    def get_pressure(self):
        return self.sensor.get_pressure()

    def get_humidity(self):
        return self.sensor.get_humidity()

    def get_temperature(self):
        return self.sensor.get_temperature()

def get_sensor_data():
    obj = Sensor()
    data = {
        "temperature": obj.get_temperature(),
        "humidity": obj.get_humidity(),
        "pressure": obj.get_pressure()
    }
    return data

if _name_ == '_main_':
    # Get sensor data
    sensor_data = get_sensor_data()

    # Save data to JSON file
    with open('sensor_data.json', 'w') as json_file:
        json.dump(sensor_data, json_file, indent=4)

    print("Sensor data has been saved to sensor_data.json")