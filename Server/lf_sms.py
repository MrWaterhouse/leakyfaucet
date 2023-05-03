#LeakyFaucet Server SMS Caller v1.2.6
#Written: Twilio Support with a few modifications by Mr.Waterhouse
#May 3, 2023
#
#This is script 3 of 4 required on the server side of LeakyFaucet.
#
#This script is called by the Filemon script and fed the phone number for messaging.
#This script is directly from Twilio support and I've just modified a few things.
#
#This script will check an authorized number list before making the SMS API call.
#If a number is presented that is not authorized, no SMS call occurs and the number is logged.
#
# Download the helper library from https://www.twilio.com/docs/python/install

#Import required modules
import os
from twilio.rest import Client
import sys
import time
import subprocess
from datetime import datetime

# Find your Account SID and Auth Token at twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']  #Get your SID from  Twilio account and use /etc/profile.d/*.sh file to export as variable
auth_token = os.environ['TWILIO_AUTH_TOKEN']    #Get your TOKEN from Twilio account and use /etc/profile.d/*.sh file to export as variable
twilio_num = os.environ['TWILIO_PHONE_SENDER']  #Get your NUMBER from Twilio account and use /etc/profile.d/*.sh file to export as variable
client = Client(account_sid, auth_token)

#Assign command-line arguments to variables. These are passed by the filemon script
phone_num = sys.argv[1]
session = sys.argv[2]
verify_mode = sys.argv[3]
print(phone_num)
print(session)
print(verify_mode)

#Assign message body variables
contact_msg = "Leaky Faucet contacted! I'll let you know how you did in 3 minutes. SessionID: "
verify_msg = " additional line(s) of data received after 3 minutes."

#Assign SMS call log files
whitelist_file = "/home/ubuntu/lf_phonelog/lf_phonewhitelist"   #If phone_num is not in this file, it will not send SMS
unauthorized_file = "/home/ubuntu/lf_phonelog/unauthAttempts.log"  #All unauthorized attempts will be logged here.
smsSent_file = "/home/ubuntu/lf_phonelog/smsSent.log"  #All authorized attempts will be logged here.
timeStamp = datetime.now()
session_dir = "/home/ubuntu/lf_exfil/"

#Read an external list of 'authorized' phone numbers and assign the contents to a variable
with open(whitelist_file) as f:
    phonewhitelist = [line.strip() for line in f]

#Check if the phone_num is in the whitelist
if phone_num in phonewhitelist and verify_mode == "0":
    # send message if phone_num is whitelisted
    message = client.messages \
                .create(
                     body=str(contact_msg) + str(session),  #"Call a plumber because you've got a leak!",
                     from_=twilio_num,
                     to='+' + phone_num
                 )
    print(message.sid)

    # write to the sms message sent log file if phone_num is whitelisted
    with open(smsSent_file, 'a') as f:
        f.write(str(timeStamp) + ' ' + str(phone_num) + ' was sent a message.\n')

else:
    # write to the unauthAttempts.log file if phone_num is not whitelisted
    with open(unauthorized_file, 'a') as f:
        f.write(str(timeStamp) + ' ' + str(phone_num) + ' attempted to receive messages.\n')

#Check if the script is in verify mode, if so run the following
if verify_mode == "1":
    #What 3 minutes before validating data received
    time.sleep(180)
    session_val = str(session_dir) + str(session) + ".txt"
    #Read how many lines are in the session file
    with open(session_val, 'r') as file:
       session_data = sum(1 for line in file)
       session_data = session_data - 1    #This is so we don't count the phone number as data.
       
    # send message with verification results
    message = client.messages \
                .create(
                     body="SessionID: " + str(session) + " had " + str(session_data) + str(verify_msg),  #"Call a plumber because you've got a leak!",
                     from_=twilio_num,
                     to='+' + phone_num
                 )
    print(message.sid)

    # write to the sms message sent log file that verification was invoked
    with open(smsSent_file, 'a') as f:
        f.write(str(timeStamp) + ' ' + str(phone_num) + ' verification process invoked.\n')