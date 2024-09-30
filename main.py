from sense_hat import SenseHat

class Sensor:
    def __init__(self):
        self.sensor = SenseHat()
        self.sensor.gain = 60
        self.sensor.integration_cycles = 256

    def get_pressure(self):
        return self.sensor.get_pressure()

    def get_humidity(self):
        return self.sensor.get_humidity()

    def get_temperature(self):
        return self.sensor.get_temperature()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    obj1 = Sensor()
    print("the current temperature is: " + str(obj1.get_temperature()))
    print("the current humidity is: " + str(obj1.get_humidity()))