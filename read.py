import time
import serial
import requests
from writer import Writer

METRICS = ["pH", "TDS", "turbidity", "temperature"]


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# ser = serial.Serial('COM6', 9600)

def get_serial():
    ser.reset_input_buffer()
    
    line = ''
    while(line == ''):
        line = ser.readline().decode('utf-8').rstrip()
    readings_list = [float(i) for i in line.split(", ")]
    Writer.append_reading(readings_list)
    readings = {}
    for i in range(4):
        readings[METRICS[i]] = readings_list[i]
    return readings


URL = 'http://192.168.1.171/data_receiver.php'
Writer.truncate()

while True:
    try:
        data = get_serial()
        print("RECEIVED\t", data)
        response = requests.post(URL, data={'data': data})
        if response.status_code == 200:
            print("success")
        else:
            print("failed to post data")
        # time.sleep(2)
    except KeyboardInterrupt:
        break

ser.close()
