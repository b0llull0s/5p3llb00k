#!/bin/bash
# 
###########################################################
#        Automatic System Updater Script                  #
#                                                         #
# Author: b0llull0s                                       #
# Original Repo: https://github.com/b0llull0s/5p3llb00k   #
# License: MIT License for original code,                 #
#          GNU General Public License (GPL) for combined  #
#          code that includes GPL licensed components     #
#                                                         #
# Description:                                            #
# This script updates the system packages for either      #
# Arch, Kali or Redhat Linux, providing the user with     #
# an option to choose between the distributions.          #
#                                                         #
# Usage:                                                  #
#   ./up.sh [Distribution]                                #
#   Supported distributions: Kali,Arch,RedHat             #
#   If no distribution is provided, the script prompts    #
#   the user to choose one.                               #
#                                                         #
# Note:                                                   #
#   This script is provided as-is without any warranties. #
#   You are free to use, modify, and distribute it.       #
#                                                         #
# GitHub: https://github.com/b0llull0s                    #
###########################################################
# Define colors
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
# Main style
echo -e "${PURPLE}Updating System${NC}"
# Update and upgrade for Kali Linux
if [[ "$1" == "Kali" ]]; then
    sudo apt update
    sudo apt upgrade -y
    sudo apt dist-upgrade -y
    sudo apt autoclean -y && sudo apt autoremove -y
    echo -e "${GREEN}Kali Linux update complete.${NC}"
# Update and upgrade for Arch Linux
elif [[ "$1" == "Arch" ]]; then
    sudo pacman -Syu --noconfirm
    echo -e "${GREEN}Arch Linux update complete.${NC}"
else
# Ask the user for the Linux distribution
    echo "Which Linux distribution do you want to update? (Kali/Arch)"
    read distribution
# Kali Loop
    if [[ "$distribution" == "Kali" ]]; then
        # Update and upgrade for Kali Linux
        sudo apt update
        sudo apt upgrade -y
        sudo apt dist-upgrade -y
        sudo apt autoclean -y && sudo apt autoremove -y
        echo -e "${GREEN}Kali Linux update complete.${NC}"
    elif [[ "$distribution" == "Arch" ]]; then
  # Arch Loop
        sudo pacman -Syu --noconfirm
        echo -e "${GREEN}Arch Linux update complete.${NC}"
  # Red Hat Loop
    elif [[ "$distribution" == "Redhat" ]]; then
        sudo yum update -y
        echo -e "${GREEN}Red Hat-based distribution update complete.${NC}"
    else
  # Invalid Error
        echo -e "${RED}Invalid option. Exiting.${NC}"
        exit 1
    fi
fi
