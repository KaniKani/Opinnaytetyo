import serial
import time
import re 

class seriallib:
    def __init__(self, port, baudarate):
        self.ser = serial.Serial(port, baudrate, timeout=2)
        time.sleep(2)
    
    def read_serial_line(self):
        line = self.ser.readline().decode('utf-8').strip()
        return line

    def read_sensor(self, sensor):
        pattern = self.read_serial_line()
        match = re.match(r"MOISTURE: (\d+); WEIGHT: (\d+)", pattern)
        if not match: 
            raise ValueError("Invalid data format: " + pattern)

        moisture = int(match.group(1))
        weight = int(match.group(2))

        if sensor.lower() == "moisture":
            return moisture
        elif sensor.lower() == "weight":
            return weight
        else:
            raise ValueError(f"Unknown sensor: {sensor}")

    def read_moisture(self):
        return self.read_sensor("moisture")

    def read_weight(self):
        return self.read_sensor("weight")
