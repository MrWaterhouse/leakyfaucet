#LeakyFaucet Server SMS Caller v1.1.0
#Written: Twilio Support with a few modifications by Mr.Waterhouse
#April 27, 2023
#
#This is script 3 of 4 required on the server side of LeakyFaucet.
#
#This script is called by the Filemon script and fed the phone number for messaging.
#This script is directly from Twilio support and I've just modified a few things.

# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import sys

# Find your Account SID and Auth Token at twilio.com/console
account_sid = "yyyyyyyyyyyyyyyyyyyyyy"   #You need to get your Twilio account SID from your user portal
auth_token = "xxxxxxxxxxxxxxxxxxxxxx" 	 #You need to get your Twilio auth token from your user portal.
client = Client(account_sid, auth_token)

# Assign target SMS phonenumber based on argument passed from Filemon script
phone_num = sys.argv[1]

message = client.messages \
                .create(
                     body="Call a plumber because you've got a leak!",
                     from_='+15555555555',     #You need to enter your Twilio phone number here.
                     to='+' + phone_num
                 )

print(message.sid)