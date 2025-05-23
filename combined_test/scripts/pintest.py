#!/usr/bin/env python3

from gpiozero import Button
from signal import pause

btn = Button(27, pull_up=False)
btn.when_pressed = lambda: print("Pin Change detected")
pause()
