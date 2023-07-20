import serial
from writer import Writer
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


METRICS = ["pH", "conductivity", "turbidity", "temperature"]



@app.route('/')
def index():
    return render_template('index.html')


class MockSerial:
    def __init__(self, *args, **kwargs):
        pass
    def readline(self):
        # return a dummy value
        return b'7.0, 100.0, 10.0, 25.0\n'
    def reset_input_buffer(self):
        pass
    def in_waiting(self):
        return True

# then use MockSerial instead of serial.Serial
ser = MockSerial('/dev/ttyACM0', 9600, timeout=1)

@app.route('/api/serial')
def get_serial():
    ser.reset_input_buffer()

    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').rstrip()
            readings_list = [float(i) for i in line.split(", ")]
            Writer.append_reading(readings_list)
            readings = {}
            for i in range(4):
                readings[METRICS[i]] = readings_list[i]
            print(readings)
            return jsonify(readings_dict=readings, message="Data fetched successfully.")
        except Exception as e:
            return jsonify(error=str(e))

    # default readings when no data from serial port
    default_readings = {
        "pH": 7.0,
        "conductivity": 50.0,
        "turbidity": 10.0,
        "temperature": 25.0
    }

    return jsonify(readings_dict=default_readings, message="Default values. No data from serial port.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
