#!/usr/bin/env python3

# Libraries
import socket
import argparse
import signal
import sys
import re
import subprocess
import os
from termcolor import colored

# Correct exit control
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del prograam...\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler) # CTRL + C

# Main menu arguments
def get_arguments():
    argparser = argparse.ArgumentParser(description="Tool to change current MAC ADDRESS")
    argparser.add_argument("-i", "--interface", dest="interface", required=True, help="Name of interface to apply new MAC ADDRESS (Ex: ens33).")
    argparser.add_argument("-m", "--mac", dest="mac_address", required=True, help="New Mac Address (Ex: 10:4b:2a:00:4f:5c).")

    arguments = argparser.parse_args()

    return arguments.interface, arguments.mac_address

def verify(interface, mac_address):

    if os.getuid() != 0:
        print(colored("\n[!] Root privilege required.\n", 'yellow')) # Verify if is running by root
        sys.exit(1)

    interfaces = [data.split(',')[1].split("'")[1] for data in map(str, socket.if_nameindex())] # Get current interfaces
    interfaces.remove("lo") # remove loopback interface
    
    interface = True if interface in interfaces else False # Validation of interface given by the user
    mac_address = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$', mac_address) # Validation of the Mac Address given by the user

    return interface and mac_address # Return True if both are correct

def change_mac_address(interface, mac_address):

    if verify(interface, mac_address):
        # Command execution using subprocess, separation by ',' when is a space (' ')
        subprocess.run(["ifconfig", interface, "down"]) # Change interface status to down
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address]) # Change Mac Adress
        subprocess.run(["ifconfig", interface, "up"]) # Change interface status to up

        print(colored(f"\n[+] Mac Address of Interface {interface} changed.\n", "green"))
    else:
        print(colored("\n[!] Incorrect Interface or Mac Address.\n", "red"))

def print_banner():
    print(colored("""

█▀▄▀█ ▄▀█ █▀▀ █▀▀ █░█ ▄▀█ █▄░█ █▀▀ █▀▀ █▀█
█░▀░█ █▀█ █▄▄ █▄▄ █▀█ █▀█ █░▀█ █▄█ ██▄ █▀▄\n""", 'white'))

    print(colored("""Mᴀᴅᴇ ʙʏ sᴀᴍᴍʏ-ᴜʟғʜ\n""", 'yellow'))

# Main logic
def main():
    print_banner()
    interface, mac_address = get_arguments()
    change_mac_address(interface, mac_address)

# Validate if the programm is running directly: ./macchanger.py
if __name__ == '__main__':
    main()
