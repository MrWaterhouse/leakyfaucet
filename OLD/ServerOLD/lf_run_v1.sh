#!/bin/bash

#LeakyFaucet Server RUN v1.0.0
#Written: Mr. Waterhouse 
#April 27, 2023
#
#This is script 4 of 4 required on the server side of LeakyFaucet.
#
#The Run bash script wipes the scratch and session data, then restarts the Listener and Filemon services. You can set a cron job to do this regularly.
#Don't forget to make your script executable with chmod +x

# 1. Search for a process containing 'lf_listener' and kill it using sudo kill
sudo pkill -f lf_listener

# 2. Search for a process containing 'lf_filemon' and kill it
pkill -f lf_filemon

# 3. Remove /home/ubuntu/pico_data.txt
rm /home/ubuntu/lf_data.txt

# 4. Clear the session log folder.
rm -f /home/ubuntu/lf_exfil/*

# 5. Create an empty /home/ubuntu/lf_data.txt file
touch /home/ubuntu/lf_data.txt

# 6. Start Listener in the background and suppress console
sudo nohup python3 /home/ubuntu/lf_listener_1.0.0.py &

# 7. Start Filemon in the background and suppress console
nohup python3 /home/ubuntu/lf_filemon_1.0.0.py &