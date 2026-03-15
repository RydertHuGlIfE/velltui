import subprocess
import colorama
from colorama import Fore, Style 
import getpass
import tuibrow

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


def send_broadcast(user, host, password):
    a = input("Enter Broadcast Message: ")
    sendbro_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} wall {a}"
    subprocess.run(sendbro_cmd, shell=True)


def check_docker_container(user, host, password):

    allcontdock_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} docker ps -a"
    contdockprunestopped_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} docker container prune"
    contdockpruneall_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} docker container prune -f"
    allimgdock = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} docker images"
    imgdockpruneall = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} docker image prune"



    

    print("\n Docker Control Menu...")
    print("1: List All Containers")
    print("2: Prune All Containers")
    print("3: List All Docker Images")
    print("4: Prune All Docker Images")
    print("5: Create a Docker image")
    print("6: Exit")
    choice = input("Enter your choice: [1/2/3/4/5/6]: ")

    if choice == "1":
        subprocess.run(allcontdock_cmd, shell=True)
    if choice == "2":
        subprocess.run(contdockprunestopped_cmd, shell=True)
    if choice == "3":
        subprocess.run(allimgdock, shell=True)
    if choice == "4":
        subprocess.run(imgdockpruneall, shell=True)
    if choice == "5":
        remote_any = tuibrow.browse_remote_any(user, host, password)
        create_docker_image = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} docker build -t {remote_any} ."
        subprocess.run(create_docker_image, shell=True)
    

