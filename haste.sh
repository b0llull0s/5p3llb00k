#!/bin/bash

IP="$1"
DIRECTORY="$2"

# mkdir
if [ ! -d "$DIRECTORY" ]; then
    mkdir "$DIRECTORY"
fi
cd "$DIRECTORY" || exit 1
# IP to /etc/hosts
echo "$IP $DIRECTORY" | sudo tee -a /etc/hosts
# Haste Nmap
nmap -sT -p- --min-rate 10000 -vvv "$IP" -oG nmap.txt

echo "$DIRECTORY deployed.Ready to pwnd."
cd "$DIRECTORY"
