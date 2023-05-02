# leakyfaucet
Python,microPython, and powershell scripts for performing data exfiltration and embedded command execution via DNS tunnel. 

There are two versions: leakyfaucet - for use from desktop OS, picowfaucet - for use with Raspberry Pi Pico W w/Pico Display v2.

This is a client/server app. You will need to register a domain name, create the required A & NS record, build a DNS listener, and have it parse out the phone number for SMS text back.

I state it directly in the scripts, but they are designed for testing. You should NOT put real data in here are you will be leaking it directly onto the internet. That's a simpleton move. Don't be a simpleton!
