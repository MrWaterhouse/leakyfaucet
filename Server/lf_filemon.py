#LeakyFaucet Server Filemon v1.2.5
#Written: Mr. Waterhouse 
#May 1, 2023
#
#This is script 2 of 4 required on the server side of LeakyFaucet.
#
#The Filemon script watches the data file created by lf_listener. As new lines appear, it parses out any phone numbers
#and send them to the SMS API caller. It also invokes a vefification check to let you know the full results.
#
#Lastly, I've built in the ability to parse out embedded bash script commands from the phonenumber query. You have to prebuild
#the bash scripts yourself or else nothing will happen.
#
#All data is written into a session specific file which can be used to manually validate the data recieved.


#Import required modules
import os
import time
import re
import subprocess

# Path to the text file to watch, the folder for session logs, and the path containing addition command calls
file_path = "/home/ubuntu/lf_data.txt"
session_dir = "/home/ubuntu/lf_exfil/"
commands_path = "/home/ubuntu/lf_commands/"

# Get the initial size of the file.
file_size = os.path.getsize(file_path)

while True:
    # Check if the file size has changed
    if os.path.getsize(file_path) > file_size:
        # Read the new line from the text file
        with open(file_path, 'r') as file:
            lines = file.readlines()
            new_line = lines[-1].strip()  # Extract the last line and remove leading/trailing whitespaces
            sessionFile = new_line[:5]  # Extract first five digits of new_line and assign to sessionFile
            new_line = new_line[5:]  # Strip off the first five digits
            file_size = os.path.getsize(file_path)  # Update the file size
            
            # Create a new file using sessionFile as the name 
            if not os.path.exists(session_dir):
                os.makedirs(session_dir)
            session_filename = os.path.join(session_dir, sessionFile + ".txt")
            with open(session_filename, "a") as f:
                f.write(new_line + "\n")

            # Check if the beginning of new_line matches the regex for 11 digit number starting with 1
            if re.match(r'^1\d{10}$', new_line[:11]):
                #Call SMS script
                phone_arg = new_line[:11] 
                subprocess.Popen(["python3", "/home/ubuntu/lf_sms.py", phone_arg, sessionFile, "0"])

                #Invoke a second SMS script in verify mode
                subprocess.Popen(["python3", "/home/ubuntu/lf_sms.py", phone_arg, sessionFile, "1"])

                #Parse out any remaining text after the phone number and try to call the matching scripts 
                command_string = new_line[11:]
                command_file = command_string + ".sh"
                try:
                   subprocess.Popen(["bash", f"{commands_path}{command_file}"])
                except FileNotFoundError:
                   print(f"No corresponding command file found in {path}.")

    # Sleep for 1 second before checking again
    time.sleep(1)