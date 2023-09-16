#!/bin/bash

#IPTABLES TO DROP
sudo iptables -F
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP
#CHECK PORTS
sudo ss -tuln  
#BLEACHBIT
read -p "Crash? (yes/no): " choice
if [[ $choice == "yes" ]]; then
        sudo bleachbit
elif [[ $choice == "no" ]]; then
    echo "Operation canceled."
fi
#PROCESS
htop
ps -auxwf
#IPTABLES ACCEPT
execute_flag="no"               #FLAG OPTION -x
while getopts "x" opt; do
  case $opt in
    x)
      execute_flag="yes"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
if [ "$execute_flag" == "yes" ]; then
  echo "Flow"
  sudo iptables -P INPUT ACCEPT
  sudo iptables -P FORWARD ACCEPT
  sudo iptables -P OUTPUT ACCEPT
fi
