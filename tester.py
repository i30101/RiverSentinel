import serial
import time
from writer import Writer
from flask import jsonify


METRICS = ["pH", "TDS", "turbidity", "temperature"]

ser = serial.Serial("COM6", 9600)

def get_serial():
    ser.reset_input_buffer()

    # if ser.in_waiting > 0:
    line = ser.readline().decode('utf-8').rstrip()
    readings_list = [float(i) for i in line.split(", ")]
    print(readings_list)
    Writer.append_reading(readings_list)
    readings = {}
    # for i in range(4):
        # readings[METRICS[i]] = readings_list[i]
    # print(jsonify(readings_dict = readings))



while True:
    get_serial()
    time.sleep(1)

