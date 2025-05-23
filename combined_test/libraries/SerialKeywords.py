from gpiozero import Device
from gpiozero.pins.rpigpio import RPiGPIOFactory
Device.pin_factory = RPiGPIOFactory() 
# ensimmäiset kolme riviä varmistavat, 
# että gpiozero käyttää oikeaa pin factorya.

import serial
import time
import re
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from time import sleep

class SerialKeywords:
    def __init__(self):
        self.outputs = {}
        self.inputs = {}
        self.ser = None

    def open_serial_connection(self, port, baudrate=115200, timeout=1):
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            print(f"Serial connection opened on {port} with baud {baudrate}")
            time.sleep(2) 
        except serial.SerialException as e:
            print(f"Failed to open serial port {port}: {e}")
            raise

    def write_to_serial(self, data):
        if self.ser and self.ser.is_open:
            self.ser.reset_input_buffer()
            print(f"Writing raw bytes: {repr(data)}")
            for char in data:
                self.ser.write(char.encode())
                time.sleep(0.01)
            self.ser.flush()

    def read_from_serial(self, timeout=3):
        if self.ser and self.ser.is_open:
            print("Reading from serial...")
            end_time = time.time() + timeout
            response = ""
            while time.time() < end_time:
                while self.ser.in_waiting > 0:
                    try:
                        line = self.ser.readline().decode(errors='ignore')
                        response += line
                    except Exception as e:
                        print(f"Read error: {e}")
                time.sleep(0.1)
            print(f"Response received: {response.strip()}")
            return response.strip()
        print("Serial not open.")
        return ""

    def close_serial_connection(self):
        if self.ser and self.ser.is_open:
            print("Closing serial connection.")
            self.ser.close()

    def reset_esp32(self):
        if self.ser and self.ser.is_open:
            print("Resetting ESP32 via DTR...")
            self.ser.setDTR(False)
            time.sleep(0.1)
            self.ser.setDTR(True)
            time.sleep(2)
    
# alla oleva koodi kehitettiin mahdollisia testejä varten, mutta niitä ei kuitenkaan tässä testiskenaariossa käytetty. 
# alla oleva koodi sisältää myös osioita aiemmista testauskohdista, jotka siirrettiin varmuuden vuoksi, vaikka niitä ei päädytty käyttämään.
# koodia ei tarvitse kommentoida ulos, sillä niitä ei kutsuta, joten ne eivät ikinä täältä käynnisty.
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

    def setup_output(self, pin):
        self.outputs[pin] = DigitalOutputDevice(int(pin))

    def setup_input(self, pin):
        self.inputs[pin] = DigitalInputDevice(int(pin))

    def write_output(self, pin, value):
        pin = int(pin)
        if pin not in self.outputs:
            self.setup_output(pin)
        device = self.outputs[pin]
        if value.lower() == "high":
            device.on()
        else:
            device.off()
    
    def read_input(self, pin):
        pin = int(pin)
        if pin not in self.inputs:
            self.setup_input(pin)
        return "HIGH" if self.inputs[pin].value else "LOW"

    def wait(self, seconds):
        sleep(float(seconds))

    def wait_for_state(self, pin, state, timeout=10):
        pin = int(pin)
        expected = 1 if state.upper() == "HIGH" else 0
        if pin not in self.inputs:
            self.setup_input(pin)
        device = self.inputs[pin]
        deadline = time() + float(timeout)
        while time() < deadline: 
            if device.value == expected: 
                return 
            wait(0.1)
        raise AssertionError(f"Pin {pin} did not reach state {state} within {timeout} seconds")
