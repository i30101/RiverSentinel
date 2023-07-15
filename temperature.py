import os
import glob
import time

# Function to read the DS18B20 sensor data
def read_ds18b20_sensor():
    # The path to the DS18B20 sensor data
    sensor_path = '/sys/bus/w1/devices/'
    sensor_folder = glob.glob(sensor_path + '28*')[0]
    sensor_file = sensor_folder + '/w1_slave'

    # Read the sensor data file
    with open(sensor_file, 'r') as file:
        lines = file.readlines()

    # Check if the data is valid
    if lines[0].strip()[-3:] != 'YES':
        return None

    # Extract the temperature from the data
    temperature_data = lines[1].strip().split('=')[-1]
    temperature_celsius = float(temperature_data) / 1000.0

    return temperature_celsius

if __name__ == '__main__':
    try:
        while True:
            temperature = read_ds18b20_sensor()
            if temperature is not None:
                print(f'Temperature: {temperature:.2f} °C')
            else:
                print('Error reading sensor data.')
            time.sleep(1)  # Read every 1 second

    except KeyboardInterrupt:
        print('Exiting...')
