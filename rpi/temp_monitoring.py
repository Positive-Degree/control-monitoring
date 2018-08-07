#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/01
#

import os
import time
import datetime
from rpi.rpi_pusher import temperature_measure_trigger

# Temp reading interval in seconds
reading_interval = 3

# Sensor ids
sensor1_id = '28-0217c038c3ff'
sensor2_id = '28-0117c052c7ff'
sensor3_id = '28-0117c01cc9ff'
sensor4_id = '28-0117c052ecff'
sensor5_id = '28-0217c067e9ff'

# Sensor associated names
sensor1_name = "water heater"
sensor2_name = "ambient temperature "
sensor3_name = "-"
sensor4_name = "-"
sensor5_name = "-"

# Contains all tempSensor objects
tempSensors = []


# Represents a physical temperature sensor (DS18B20 connected to the rpi)
class TempSensor:

    # path where the sensor devices files are localized on the pi
    rpi_base_dir = '/sys/bus/w1/devices/'

    def __init__(self, sensor_id, sensor_name):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.sensor_folder = self.rpi_base_dir + self.sensor_id
        self.sensor_file = self.sensor_folder + '/w1_slave'
        self.current_temperature = 0.0

        # Adds itself to the sensors list
        tempSensors.append(self)

    # Updates its current temperature reading
    def update_temp(self):
        self.current_temperature = self.read_temp()

    # Reads the temperature measured by the sensor
    def read_temp(self):

        # Reads the raw info in the file
        def read_raw_temp():
            f = open(self.sensor_file, 'r')
            raw_lines = f.readlines()
            f.close()
            return raw_lines

        # Catches exception if one of the sensors is not connected
        try:
            lines = read_raw_temp()
        except IOError:
            return self.sensor_name, "The sensor is not connected."

        # Identifies the temp info
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_raw_temp()
        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_celsius = float(temp_string) / 1000.0
            # temp_fahrenheit = temp_c * 9.0 / 5.0 + 32.0
            return temp_celsius


# Updates the current temperature reading of the sensors
def update_sensors():
    for sensor in tempSensors:
        sensor.update_temp()


# Creates and logs the measured temperatures of the sensors in a txt file on the rpi
def log_temps():

    rpi_log_dir = '/home/pi/Documents/PositiveDegree/tempLogs/'
    current_date = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    logfile = open(rpi_log_dir + current_date + ".txt", "a+")

    logfile.write("--------------------------- \n")

    for sensor in tempSensors:
        current_time = str(datetime.datetime.now().time())
        sensor_name = str(sensor.sensor_name)
        sensor_temp = str(sensor.current_temperature)
        logfile.write(sensor_name + " : " + sensor_temp + " | " + current_time + "\n")

    logfile.close()


# Updates the temperature measures for the Pusher subscribers
def push_temps():

    for sensor in tempSensors:
        temperature_measure_trigger(sensor.sensor_id, sensor.sensor_name, sensor.current_temperature)


def main():
    # Creates all the sensors
    sensor1 = TempSensor(sensor1_id, sensor1_name)
    sensor2 = TempSensor(sensor2_id, sensor2_name)
    # sensor3 = TempSensor(sensor3_id, sensor3_name)
    # sensor4 = TempSensor(sensor4_id, sensor4_name)
    # sensor5 = TempSensor(sensor5_id, sensor5_name)

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    # Shows temps every x amount of time
    while True:
        update_sensors()
        print(sensor1.current_temperature)
        print(sensor2.current_temperature)
        # log_temps()
        push_temps()
        time.sleep(reading_interval)


if __name__ == "__main__":
    main()
