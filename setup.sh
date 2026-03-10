#!/bin/bash

echo "Setting up VELLTUI dependencies..."

if [ -f /etc/arch-release ]; then
    sudo pacman -S --needed rsync sshpass python-colorama
    sudo pacman -S --needed btop 
elif [ -f /etc/debian_version ]; then
    sudo apt update
    sudo apt install -y rsync sshpass python3-colorama
    sudo apt install btop

elif [-f /etc/fedora_version]; then 
    sudo dnf install -y rsync sshpass python3-colorama
    sudo dnf install btop 
else
    echo "Unsupported OS. Please install rsync, sshpass and colorama manually."
    exit 1
fi

echo "Setup complete. Run 'python3 main.py' to start."
