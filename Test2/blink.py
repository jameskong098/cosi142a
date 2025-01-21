from time import sleep
from machine import Timer
from machine import Pin

pin = Pin(20, Pin.OUT)
print("LED starts flashing...")

def blink(timer):
    pin.toggle()

timer = Timer()
timer.init(freq=10, mode=Timer.PERIODIC, callback=blink)
tim = Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))