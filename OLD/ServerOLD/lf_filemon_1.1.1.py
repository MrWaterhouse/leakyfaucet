#LeakyFaucet Server Filemon v1.1.1
#Written: Mr. Waterhouse 
#April 28, 2023
#
#This is script 2 of 4 required on the server side of LeakyFaucet.
#
#The Filemon script watches the data file created by lf_listener. As new lines appear, it parses out any phone numbers and send them to the SMS API caller.
#All data is written into a session specific file which can be used to manually validate the data recieved.


#Import required modules
import os
import time
import re
import subprocess

# Path to the text file to watch, and the folder for session logs
file_path = "/home/ubuntu/lf_data.txt"
file_dir = "/home/ubuntu/lf_exfil/"

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
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            filename = os.path.join(file_dir, sessionFile + ".txt")
            with open(filename, "a") as f:
                f.write(new_line + "\n")

            # Check if the new line matches the regex for 11 digit number starting with 1
            if re.match(r'^1\d{10}$', new_line):
                #Call SMS script 
                subprocess.call(["python3", "/home/ubuntu/lf_sms_1.2.0.py", new_line])

    # Sleep for 1 second before checking again
    time.sleep(1)