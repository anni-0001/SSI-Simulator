import subprocess
import os 
import time
import pickle


os.chdir("/icmp")
# get ip address from server and run it in the server?

session_name = "icmp_session_server"
# Start a new tmux session
subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
time.sleep(1)  # Wait for tmux session to initialize

# Send the command to start ptunnel
time.sleep(10)

# start session on server
cmd = "ptunnel-ng"
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)
