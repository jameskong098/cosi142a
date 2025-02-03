from machine import I2C, Pin
import time
from lcd1602 import LCD1602

# Initialize I2C0
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)

# Scan for I2C devices
devices = i2c.scan()
if not devices:
    raise Exception("No I2C devices found")
#else:
    #print("I2C devices found:")
    '''
    for device in devices:
        print(hex(device))
    '''

# Assuming the first device found is the LCD
lcd_address = hex(devices[0])

# Initialize the LCD1602 display with the found address
lcd = LCD1602(i2c, lines=2, dotsize=LCD1602.LCD_5x8DOTS)

# Initialize the button on D20
button = Pin(20, Pin.IN, Pin.PULL_UP)

# Flag to indicate if the LCD should be cleared
clear_lcd_flag = False

def clear_handler(pin):
    lcd.clear()
    print("Cleared!")

# Attach an interrupt to the button pin
button.irq(trigger=Pin.IRQ_FALLING, handler=clear_handler)

def print_message(message):
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.print(message[:16])  # Print the first 16 characters on the first line
    if len(message) > 16:
        lcd.setCursor(0, 1)
        lcd.print(message[16:32])  # Print the next 16 characters on the second line

# Keep the program running
while True:
    user_input = input("Enter a message to print on the LCD: ").strip()
    if user_input:
        print_message(user_input)
    else:
        print("Invalid input. Please enter a non-empty message.")
    time.sleep(0.1)