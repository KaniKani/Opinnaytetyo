import serial
import time

port = '/dev/ttyUSB0'
baudrate = 115200

ser = serial.Serial(port, baudrate, timeout=1)
time.sleep(2)

ser.write(b'h')

response = ser.readline().decode().strip()
print(f"Response: {response}")

ser.close()
