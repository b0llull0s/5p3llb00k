#!/bin/bash
# b0llull0s@P4n1cThr3ads 
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
    else
  # Invalid Error
        echo -e "${RED}Invalid option. Exiting.${NC}"
        exit 1
    fi
fi
