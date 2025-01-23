from machine import ADC, Pin, PWM
import time

adc = ADC(Pin(26))
# create PWM object from a pin and set the frequency
pwmO = PWM(Pin(20), freq=2000)

try:
    while True:
        print(adc.read_u16())
        # Change the duty cycle of the PWM signal based on the ADC value 
        pwmO.duty_u16(adc.read_u16())
        time.sleep(0.2)
except KeyboardInterrupt:
    pass