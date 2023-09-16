!#/bin/bash


#IPTABLES TO DROP
sudo iptables -F
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP
#MONITORING
sudo ss -tuln           
htop
wireshark&
#BLEACHBIT
read -p "Do you want to run 'sudo bleachbit'? (yes/no): " choice
if [[ $choice == "yes" ]]; then
        sudo bleachbit
elif [[ $choice == "no" ]]; then
    echo "Operation canceled."
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
  echo "Executing commands because -x option was provided."
  sudo iptables -P INPUT ACCEPT
  sudo iptables -P FORWARD ACCEPT
  sudo iptables -P OUTPUT ACCEPT