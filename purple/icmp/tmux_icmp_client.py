
import subprocess
import os 
import time

os.chdir("/icmp")
# get ip address from server and run it in the server?

session_name = "icmp_session_client"
# Start a new tmux session
subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
time.sleep(1)  # Wait for tmux session to initialize

cmd = 'sleep 10'
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)
time.sleep(10)


# start client command to connect to server, ip is different: 
cmd = "ptunnel-ng -p 172.20.0.2 -l8888"
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)



time.sleep(5)

# client command in seperate tmux window to connect via ssh thru icmp:
cmd = "ssh -p8888 -l ssh_user 127.0.0.1 "
subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

# time.sleep(15)

# Attach to the tmux session
subprocess.run(f"tmux attach -t {session_name}", shell=True)


# server: ptunnel-ng 

# client
# ptunnel-ng -p <server ip> -l 8888
# in new window:
    # ssh -p8888 -l ssh_user 127.0.0.1


