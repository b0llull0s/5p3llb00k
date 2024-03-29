#!/bin/bash
#IPTABLES TO DROP
sudo iptables -F
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP
#IPTABLES ACCEPT
execute_flag="no"               #FLAG OPTION -x
while [[ $# -gt 0 ]]; do
    case "$1" in
        -x)
            execute_flag="yes"
            shift
            ;;
        *)
            echo "Invalid option: $1" >&2
            exit 1
            ;;
    esac
done
if [ "$execute_flag" == "yes" ]; then
    echo "Flow"
    sudo iptables -P INPUT ACCEPT
    sudo iptables -P FORWARD ACCEPT
    sudo iptables -P OUTPUT ACCEPT
    exit
fi
#CHECK PORTS
ss -tuln  
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
