#!/bin/bash

#LeakyFaucet Server RUN v3
#Written: Mr. Waterhouse 
#May 1, 2023
#
#This is script 4 of 4 required on the server side of LeakyFaucet.
#
#The Run bash script wipes the scratch and session data, then restarts the Listener and Filemon services. You can set a cron job to do this regularly.

# 1. Search for a process containing 'lf_listener' and kill it using sudo kill
sudo pkill -f lf_listener

# 2. Search for a process containing 'lf_filemon' and kill it
pkill -f lf_filemon

# 3. Remove /home/ubuntu/pico_data.txt
rm /home/ubuntu/lf_data.txt

# 4. Create an empty /home/ubuntu/lf_data.txt file
touch /home/ubuntu/lf_data.txt

# 5. Clear nohup data since some data may end up in there
rm /home/ubuntu/nohup.out

# 6. Clear out the exfil log folder. (Do not delete files younger than 10 minutes in case it is still in active verification.)
find /home/ubuntu/lf_exfil/* -mmin +10 -type f -print0 | xargs -0 rm -f

# 7. Start Listener in the background and suppress console
sudo nohup python3 /home/ubuntu/lf_listener_1.0.0.py &

# 8. Start Filemon in the background and suppress console
nohup python3 /home/ubuntu/lf_filemon.py &
