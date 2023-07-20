import serial
from writer import Writer
from flask import Flask, render_template, jsonify


app = Flask(__name__)


METRICS = ["pH", "TDS", "turbidity", "temperature"]



@app.route('/')
def index():
    return render_template('index.html')




ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

@app.route('/api/serial')
def get_serial():
    ser.reset_input_buffer()

    line = ser.readline().decode('utf-8').rstrip()
    readings_list = [float(i) for i in line.split(", ")]
    print(readings_list)
    Writer.append_reading(readings_list)
    readings = {}
    for i in range(4):
        readings[METRICS[i]] = readings_list[i]
    return jsonify(readings_dict = readings)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
