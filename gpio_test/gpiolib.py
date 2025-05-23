from gpiozero import DigitalInputDevice, DigitalOutputDevice
from time import sleep

class gpiolib:
    def __init__(self):
        self.outputs = {}
        self.inputs = {}

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

    def sleep(self, seconds):
        sleep(float(seconds))
