import network
import socket
import time
from machine import Pin, I2C
from lcd1602 import LCD1602

# Wi-Fi credentials
ssid = 'COSI142-a'
password = 'embedded_systewm'

# Initialize I2C0
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)

# Scan for I2C devices
devices = i2c.scan()
if not devices:
    raise Exception("No I2C devices found")

lcd_address = hex(devices[0])
lcd = LCD1602(i2c, lines=2, dotsize=LCD1602.LCD_5x8DOTS)

button = Pin(20, Pin.IN, Pin.PULL_UP)

clear_lcd_flag = False

def print_message(message):
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.print(message[:16])  
    if len(message) > 16:
        lcd.setCursor(0, 1)
        lcd.print(message[16:32]) 

def webpage():
    html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>LCD Controller</title>
            </head>
            <body>
                <h1>LCD Controller</h1>
                <form action="./send" method="post">
                    <input type="text" name="message" placeholder="Enter message">
                    <button type="submit" name="action" value="send">Send</button>
                </form>
                <form action="./clear" method="post">
                    <button type="submit" name="action" value="clear">Clear</button>
            </body>
        </html>
        """
    return str(html)

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for Wi-Fi connection
connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# Check if connection is successful
if wlan.status() != 3:
    raise RuntimeError('Failed to establish a network connection')
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])

# Set up socket and start listening
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

print('Listening on', addr)

state = "OFF"
while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        request = conn.recv(1024).decode('utf-8')  
        print('Request content =', request)

        try:
            request_path = request.split()[1]
            print('Request:', request_path)
        except IndexError:
            request_path = ""

        if "POST" in request:
            content_start = request.find("\r\n\r\n") + 4  
            post_data = request[content_start:].strip()  
            
            print("Post Data:", post_data) 

            if "message=" in post_data:
                message = post_data.split("message=")[1].split("&")[0]  
                message = message.replace("+", " ").replace("%20", " ")  
                
                print("Extracted Message:", message)  
                print_message(message)  

            elif "clear" in post_data:
                lcd.clear()

        response = webpage()  
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')
