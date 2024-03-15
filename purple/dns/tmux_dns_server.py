import subprocess
import os 
import time
import pexpect
import socket



hostname = socket.gethostname()
print("Hostname:", hostname)

if hostname == 'server':
    # Change to the directory where dnscat2.rb is located
    os.chdir("/dns/server")

    session_name = "dns_session_server"

    # Start a new tmux session
    subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
    time.sleep(1)  # Wait for tmux session to initialize

    # Send the command to start dnscat2
    cmd = "ruby dnscat2.rb --secret=abc"
    subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

    # subprocess.run(f"tmux attach -t {session_name}", shell=True)

    # Wait for dnscat2 to start
    # time.sleep()
    time.sleep(10)

# # Attach to the tmux session to interact with dnscat2
# tmux_process = pexpect.spawn(f'tmux attach -t {session_name}')
# time.sleep(5)
# # Wait for dnscat2 prompt
# tmux_process.expect('dnscat2>')
# time.sleep(15)
# # tmux_process.sendline('')

# # Send commands using Pexpect
# tmux_process.sendline('session -i 1')
# # tmux_process.sendline('')  # Send an "Enter" key press
# time.sleep(3)
# tmux_process.expect('dnscat2>')
# # tmux_process.sendline('')  # Send an "Enter" key press

# print("Session 1 initiated")
# time.sleep(5)
# tmux_process.sendline('shell')
# # tmux_process.sendline('')  # Send an "Enter" key press


# tmux_process.expect('dnscat2>')
# # tmux_process.sendline('')  # Send an "Enter" key press

# print("Shell session started")
# time.sleep(5)
# tmux_process.sendline('session -i 2')
# tmux_process.sendline('')  # Send an "Enter" key press

# time.sleep(3)
# tmux_process.expect('dnscat2>')
# print("Session 2 initiated")

# time.sleep(5)
# tmux_process.sendline('ls')


# # Continue with other commands if needed
# # tmux_process.sendline('your_next_command_here')
# # tmux_process.expect('dnscat2>')

# # Close the connection
# tmux_process.close()
# print("Connection closed")

# cmd = 'sleep 3'
# subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)


# cmd = "session -i 1"
# subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

# cmd = "shell"
# # session -i 2
# subprocess.run(f'tmux send-keys -t {session_name} "{cmd}" Enter', shell=True)

# cmd = "ls"

# # Attach to the tmux session
subprocess.run(f"tmux attach -t {session_name}", shell=True)

# # weird session managemtn retry