#!/usr/bin/python3

import sys
import subprocess
import time
import pexpect
from pexpect import popen_spawn
from pexpect import pxssh
#import paramiko

if len(sys.argv) < 6:
    raise UserWarning("Please use six or more parameters")

device_num = sys.argv[1]
experiment_num = sys.argv[2]
scan_time = sys.argv[3]
devices = sys.argv[4]
action = sys.argv[5]
tunnel_type = sys.argv[6]
brk=3

breaks=[]

port=22
target=int(devices)
step=int(device_num)+1
target_ip="172.50.0."+str(step+1)

#print("This is print "+target_ip)
#subprocess.Popen(f"echo This is subprocess {target_ip}", shell=True)

sshtunnel=""

#with open("/opt/config", "w+") as config:
#    for line in config
#    breaks.append(line)

def get_commands(cmdfile):
    cmds=[]
    with open(cmdfile, 'r') as cf:
        for cmd in cf:
            cmds.append(cmd)
    #print(cmds)
    return cmds

def http_tunnel(target, experiment_num):
    http = subprocess.Popen("/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    http.communicate(str("sudo timeout "+scan_time+" bash /opt/net-start.sh "+str(target)+" "+experiment_num).encode())
    #subprocess.run("sudo bash /opt/net-test.sh "+target_ip)

def ssh_tunnel(start, target, port):
    proxy=""
    while start <= target:
        if start == target:
            proxy=proxy+"root@dev"+str(start)
        elif start == target-1:
            proxy=proxy+"root@dev"+str(start)+" "
        else:
            proxy=proxy+"root@dev"+str(start)+","
        start=start+1
    with open("/purple/results/testy.txt", 'w+') as testy:
        testy.write(f"Parameters: Start: {start}, Target: {target}, Port: {port}, Proxy: {proxy}")
    tunnel = subprocess.Popen("/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #tunnel.communicate(str("sudo timeout "+scan_time+" bash /opt/ssh-connect.sh "+proxy+ " "+experiment_num).encode())
    tunnel.communicate(f"sudo timeout {scan_time} bash /opt/ssh-connect.sh {proxy} {experiment_num} >> /purple/results/{experiment_num}/results.txt".encode())


def build_tunnel(tunnel_type):
    #For right now aussme the first tunnel is nc

    #For any tunnel of n>=3 i[0]=1, i[1]=2, i[2]=3, even if i[3]=n. A special cases cases will be added later for n=1 and n=2
    
    #This Funtion is currently based on the principle of a nested comd (ssh nc ssh nc) for tunnel interlopability
    #This Funciton specifcally buildislis a string based on agiven array of what protcol each inter-node tunnel will use
    #This string is currently just executed, but there should be a third script to handle feeding commands to it (as SSH ahas no
    #wrapper script
    cmd="sudo timeout "+scan_time+" bash /opt/nt.sh dev2 "+experiment_num+" 0"
    i=3

    for tunnel in tunnel_type:
        if tunnel == "ssh":
            cmd = cmd+" ssh dev"+str(i)
        elif tunnel == "nc":
            if i == int(devices):
                cmd == cmd+" /opt/nt.sh dev"+str(i)+" "+experiment_num+" 1 /bin/bash"
            else:
                cmd = cmd+" /opt/nt.sh dev"+str(i)+" "+experiment_num+" 1"
        else:
            raise UserWarning("please provide appropiately formated sequence")
        i=i+1

    print(cmd)
    with open("/purple/results/prelim", 'w+') as prelim:
        prelim.write(cmd)
    subprocess.run(cmd, shell=True)


    #if tunnel_type == 0:
    #    print("SSH TUNNEL")
    #    ssh_tunnel(1, target, 22)
    #elif tunnel_type == 1:
    #    http_tunnel(step, experiment_num)
    #else:
    #    print("Please Select at tunnel")


#+=======Main method=========+

subprocess.run("service ssh restart", shell=True)
#subprocess.run("timeout 10 tcpdump -i eth0 -U -w /purple/tcpdump/"+experiment_num+"/dev"+device_num+".pcap &", shell=True)

#---The following helps to intialize the execution while starting a tcpdump on dev1, it is a bit hacky right now, investiagte
#better soultions as well---"

#print(target)

if int(device_num) == 1 and int(action) != 1:
    subprocess.run("timeout 10 tcpdump -i eth0 -U -w /purple/tcpdump/"+experiment_num+"/dev"+device_num+".pcap &", shell=True)
    #isubprocess.run("sudo /bin/bash -c /opt/listener.sh "+device_num+" "+experiment_num+" purple", shell=True)
    tmp = subprocess.Popen("/bin/bash", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    tmp.communicate(f"python3 /opt/alt_internal.py {device_num} {experiment_num} {scan_time} {devices} 1 {tunnel_type}".encode())
    time.sleep(int(scan_time))
elif int(action) == 1:
    print("New Connection")
    #http_tunnel(str(target_ip), experiment_num)
    build_tunnel(["ssh", "nc", "ssh"])
else:
    subprocess.run(f"sudo timeout {scan_time} bash /opt/listener.sh {device_num} {devices} {experiment_num} {brk} purple", shell=True)
    subprocess.run("sudo service restart ssh", shell=True)
    subprocess.run("timeout 10 tcpdump -i eth0 -U -w /purple/tcpdump/"+experiment_num+"/dev"+device_num+".pcap &", shell=True)
    if int(device_num) == int(devices):
        with open("/opt/bob", 'w+') as b:
            b.write("This is a secret\n")
        with open("/opt/alice", 'w+') as a:
            a.write("This is another secret\n")
        with open("/opt/eve", 'w+') as e:
            e.write("And rounding out the group\n")
        subprocess.run("ls /opt", shell=True)
    time.sleep(int(scan_time))
