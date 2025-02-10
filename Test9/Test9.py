from machine import ADC, Pin, PWM
import time

# Initialize ADC for the potentiometer
adc = ADC(Pin(26))

# Initialize PWM for the RGB LED
pwmR = PWM(Pin(20), freq=2000)  # Red
pwmG = PWM(Pin(21), freq=2000)  # Green
pwmB = PWM(Pin(22), freq=2000)  # Blue

try:
    while True:
        # Read the ADC value from the potentiometer
        adc_value = adc.read_u16()
        
        # Map the ADC value to PWM duty cycle (0-65535)
        duty_cycle = adc_value
        
        # Set the duty cycle for each color based on the ADC value
        pwmR.duty_u16(duty_cycle)
        pwmG.duty_u16(65535 - duty_cycle)
        pwmB.duty_u16(duty_cycle // 2)
        
        print(f"ADC Value: {adc_value}, Duty Cycle: {duty_cycle}")
        time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    # Deinitialize PWM
    pwmR.deinit()
    pwmG.deinit()
    pwmB.deinit()