import serial
import time

class SerialKeywords:
    def __init__(self):
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
