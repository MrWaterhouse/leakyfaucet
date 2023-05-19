# leakyfaucet - A multiuser DNS Exfiltration Proof-of-Concept With Optional Asynchronous SMS Messaging and AI Integration
Leakyfaucet is a client/server DNS exfiltration tool for testing security products. At it's lowest requirements, you need one of the client scripts and the lf_listener.py script on a server. If you install all of the server components, the server can send you replies out-of-band via SMS message. This give security mechanisms one less communications channel to scan.

This is NOT a command-and-control DNS Tunnel solution. It is specifically designed to allow for exfiltration of data by one or more users at a time. It tracks each individaul exfiltration session so the data doesn't get mixed together. As stated above, I also built in the ability to embed queries for an AI engine - the replies will be sent back via SMS. So as long as you can get as few as two DNS queries out the door, you can use AI. 

Scripts:

Client

  leakyfaucet.py - Python script that accepts your phone number, and domain as cli arguments. It send 4 pieces of dummy data.

  leakyfaucetai.py - Interactive python script that asks you for all required data. You can also use the ai switch at the cli.
  
  leakyfaucet.ps1 - Powershell version of the cli argument script for use on Windows systems (cannot do ai queries).
  
  picofaucet.py - Micropython version designed to run on a raspberry pi pico w. Send 4 pieces of dummy data and requires secrets.py
  
  secrets.py - SSID and Password file for picofaucet.py. You need to replace the dummy info with your WLAN info.
  
  stagedfaucet.py - Python script that you can point a staged text file containing data to exfil via dns. 

Server
  
  lf_listener.py - DNS listener for server. If all you want is to catch the data, this is all you need to run.
  
  lf_filemon.py - Monitors for captured data, reorganize it, call the sms scripts, and commands script like ai.
  
  lf_sms.py - SMS messaging script for Twilio integration. If you want a reply, you need this.
  
  lf_run.sh - Clean up script you can run with crontab to periodically clean up gathered data.
  
If you inspect the client scripts you'll see that you can also add a command string (ie. ai) and the server will try to execute a bash file matching that name for you. You will need to build out your own bash scripts. Currently, to prove out the functionality, I've successfully run a script for ChatGPT integration and scan scripts. The sky is the limit.

Requirements: You will need a client, a server (I am using Ubuntu), a domain name, and the ability to setup your NS records. If you want to use the SMS and AI functions, you will need Twilio (or another service) and an AI API account.

Warning!
I state it directly in the scripts, but they are designed for testing. You should NOT put real data in here are you will be leaking it directly onto the internet. That's a simpleton move. Don't be a simpleton!
