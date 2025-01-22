from machine import ADC, Pin
import time

adc = ADC(Pin(26))
try:
    while True:
        print(adc.read_u16())
        time.sleep(1)
except KeyboardInterrupt:
    pass