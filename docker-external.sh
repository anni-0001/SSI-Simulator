#!/bin/bash
TOTAL_ROUNDS=2 
SCAN_TIME=60
devices=4
dir=$(pwd)
RES_DIR=${dir}/results
networkName="SSID"
subnet="172.50.0.0/24"
gateway="172.50.0.254"
#VERSION_DIR=SSH_TCP_MODEL

round=1
# look into building standard docker image
#

echo "---docker-external.sh---"
if [ $# -eq 0 ]; then 

    echo " "
    read -p "Enter max number of hosts: " devices
    read -p "Enter timeout duration: " SCAN_TIME
    read -p "Enter experiment rounds: " TOTAL_ROUNDS
else 

    if [ "$1" == "static" ]; then 
        TOTAL_ROUNDS=2
        SCAN_TIME=300
        devices=4
    else
        devices=$1
        SCAN_TIME=$2
	TOTAL_ROUNDS=$3
    fi
fi


# configutaions for:
#     - ssh config   
#     - uniform device numbers in dev-num.txt
#     - docker-compose
#     - uniform SCAN_TIME

# creates automated ssh config for x number of devices
bash ssh-config.sh $devices
echo ""
echo "CONFIGURATIONS"
echo "Device Number: $devices"
echo "SCAN_TIME: $SCAN_TIME"
echo "Rounds: $TOTAL_ROUNDS"

echo ""

# makes uniform scan_time vars in .env for all experiements
touch .env
# sed -i "1c\\SCAN_TIME=$SCAN_TIME" .env

while [ $round -le $TOTAL_ROUNDS ]
do
    #service docker restart
    docker network prune -f
    # echos current round into round.txt for uniform variable useage
    echo $round > round.txt

    # create docker-compose.yml script
    dev_count=$(shuf -i 3-$devices -n 1)
    echo " [*] Create docker-compose.yaml with $dev_count hosts"
    bash compose-bash.sh $dev_count $round $SCAN_TIME $subnet $gateway $networkName

    echo " [*] Running round $round..."
   
    # create exp tcpdump dir

    echo " [*] making directory: $round"
    mkdir -p ${RES_DIR}/${round}

    # start up docker containers
    echo "---create env---"
    # docker compose up --build --quiet
    docker compose up --build --wait

    echo "---dev1 log---"
    # wait till dev1 is done 
    docker attach --no-stdin dev1
    echo $(docker logs dev1)
    exitcode=$(docker wait dev1)
    echo " [*] dev1 exited with $exitcode"
    echo " [*] stopping & removing containers"

    # stop and delete all active containers
    docker compose down
    sleep 10
    # increase sleep for overnight


    ((round ++))
done 
sleep 5

# gets correct # of rounds run
finalround=$(cat round.txt)

echo " [*] docker-external.sh finished -- $finalround experiments complete"

# look at how to set things up for commmands
# replace static commands - select random command - randomly sample send & recieve
# sending dummy commands to create & send data - send 100 bytes as a command
# want to recieve x data size

# build loop to sample & identify numbers/stats we want to see - read from csv
# pasrse from file, select random row (command), acces range entries, smaple bytes of random between 2 ranges, send command

# on victim machine set up sinlge caharacter alias to bash oneliner to shorten the minimum number of bytes & fill in the rest with gibberish to fill random range
