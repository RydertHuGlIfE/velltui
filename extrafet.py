import subprocess
import colorama
from colorama import Fore, Style 
import getpass


colorama.init(autoreset=True)

def system_monitor(user, host, password):
    # -tt forces TTY allocation for the UI
    # -o StrictHostKeyChecking=no skips the hidden "yes/no" prompt
    btop_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} btop"
    
    # Run interactively so the UI appears in your terminal
    subprocess.run(btop_cmd, shell=True)

    
