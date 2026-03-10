import subprocess
import colorama
from colorama import Fore, Style 
import getpass


colorama.init(autoreset=True)

def system_monitor(user, host, password):
    btop_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} btop"
    subprocess.run(btop_cmd, shell=True)

    
