import subprocess
import colorama
from colorama import Fore, Style 
import getpass


colorama.init(autoreset=True)

def system_monitor(user, host, password):
    btop_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} btop"
    subprocess.run(btop_cmd, shell=True)


def remote_shell(user, host, password):
    shell_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} zsh"
    subprocess.run(shell_cmd, shell=True)


def server_control(user, host, password):
    print("\n Server Control Menu... ")
    print("1: Reboot Server")
    print("2: Shutdown Server")
    print("3: Exit")
    choice = input("Enter your choice: [1/2/3]: ")

    if choice == "1":
        reboot_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} sudo reboot"
        subprocess.run(reboot_cmd, shell=True)
    if choice == "2":
        shutdown_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} sudo shutdown now"
        subprocess.run(shutdown_cmd, shell=True)
    if choice == "3":
        return


def check_logs(user, host, password):
    checklog_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} journalctl -f"
    subprocess.run(checklog_cmd, shell=True)