import machine
import utime

# Initialize ADC (Analog to Digital Converter) for the sound sensor
sound_sensor = machine.ADC(27)  # Assuming the sound sensor is connected to pin 25

def read_sound():
    # Read the analog value from the sound sensor
    sound_level = sound_sensor.read_u16()
    return sound_level

while True:
    sound_level = read_sound()
    print("Sound Level:", sound_level)
    utime.sleep(1)  # Wait for 1 second before reading again