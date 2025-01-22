from machine import Pin, PWM
from utime import sleep

# create PWM object from a pin and set the frequency
pwmO = PWM(Pin(20), freq=2000)

try:
    while True:
        # Increase duty cycle from 0 to 65535
        for duty in range(0, 65536, 256):
            pwmO.duty_u16(duty)
            sleep(0.002)  
        # Decrease duty cycle from 65535 to 0
        for duty in range(65535, -1, -256):
            pwmO.duty_u16(duty)
            sleep(0.002)  
except KeyboardInterrupt:
    pass

pwmO.deinit()