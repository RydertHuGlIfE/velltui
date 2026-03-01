#!/bin/bash

echo "Setting up RSTUI dependencies..."

if [ -f /etc/arch-release ]; then
    sudo pacman -S --needed rsync sshpass python-colorama
elif [ -f /etc/debian_version ]; then
    sudo apt update
    sudo apt install -y rsync sshpass python3-colorama
else
    echo "Unsupported OS. Please install rsync, sshpass and colorama manually."
    exit 1
fi

echo "Setup complete. Run 'python3 main.py' to start."
