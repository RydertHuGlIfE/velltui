import subprocess
import colorama
from colorama import Fore, Style 
import getpass
import tuibrow

colorama.init(autoreset=True)

def system_monitor(user, host, password):
    btop_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} btop"
    btop_force_utf = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} btop --force-utf"
    try:
        subprocess.run(btop_cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        subprocess.run(btop_force_utf, shell=True)


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

    base_ssh = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host}"
    mac_paths = "/usr/local/bin:/opt/homebrew/bin:~/.docker/bin:/Applications/Docker.app/Contents/Resources/bin"

    allcontdock_cmd = f"{base_ssh} docker ps -a"
    allcontdock_mac = f"{base_ssh} 'export PATH=$PATH:{mac_paths} && docker ps -a'"

    contdockprunestopped_cmd = f"{base_ssh} docker container prune"
    contdockprunestopped_mac = f"{base_ssh} 'export PATH=$PATH:{mac_paths} && docker container prune'"

    contdockpruneall_cmd = f"{base_ssh} docker container prune -f"
    contdockpruneall_mac = f"{base_ssh} 'export PATH=$PATH:{mac_paths} && docker container prune -f'"

    allimgdock = f"{base_ssh} docker images"
    allimgdock_mac = f"{base_ssh} 'export PATH=$PATH:{mac_paths} && docker images'"

    imgdockpruneall = f"{base_ssh} docker image prune"
    imgdockpruneall_mac = f"{base_ssh} 'export PATH=$PATH:{mac_paths} && docker image prune'"

    print("\n Docker Control Menu...")
    print("1: List All Containers")
    print("2: Prune All Containers")
    print("3: List All Docker Images")
    print("4: Prune All Docker Images")
    print("5: Create a Docker image")
    print("6: Exit")
    choice = input("Enter your choice: [1/2/3/4/5/6]: ")

    if choice == "1":
        try:
            subprocess.run(allcontdock_cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run(allcontdock_mac, shell=True)
    if choice == "2":
        try:
            subprocess.run(contdockprunestopped_cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run(contdockprunestopped_mac, shell=True)
    if choice == "3":
        try:
            subprocess.run(allimgdock, shell=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run(allimgdock_mac, shell=True)
    if choice == "4":
        try:
            subprocess.run(imgdockpruneall, shell=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run(imgdockpruneall_mac, shell=True)
    if choice == "5":
        remote_any = tuibrow.browse_remote_any(user, host, password)
        if not remote_any:
            print("No path selected.")
            return

        image_name = input("Enter Image Name (tag, e.g., my-app:v1): ").strip()
        if not image_name:
            image_name = "my_remote_image:latest"

        if remote_any.endswith("/"):
            build_ctx = remote_any
            docker_cmd = f"docker build -t {image_name} {build_ctx}"
        else:
            parts = remote_any.rsplit("/", 1)
            build_ctx = parts[0] + "/" if len(parts) == 2 else "."
            docker_cmd = f"docker build -t {image_name} -f {remote_any} {build_ctx}"

        create_docker_image = f"{base_ssh} '{docker_cmd}'"
        create_docker_image_mac = f"{base_ssh} 'export PATH=$PATH:{mac_paths} && {docker_cmd}'"
        
        print(Fore.YELLOW + f"Executing on remote: {docker_cmd}" + Style.RESET_ALL)
        try:
            subprocess.run(create_docker_image, shell=True, check=True)    
        except subprocess.CalledProcessError:
            subprocess.run(create_docker_image_mac, shell=True)



def view_files_vim(user, host, password):
    remote_a = tuibrow.browse_remote_any(user, host, password)
    if not remote_a:
        print("No Path Selected... ")
        return 

    vimssh = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} nvim {remote_a}"
    subprocess.run(vimssh, shell=True)


def disk_usage_analyzer(user, host, password):
    current_path = "/"
    while True:
        print(Fore.CYAN + f"\n Analyzing Disk Usage at: {current_path}" + Style.RESET_ALL)
        cmd = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {user}@{host} \"du -h --max-depth=1 {current_path} 2>/dev/null | sort -hr\""
        
        try:
            result = subprocess.check_output(cmd, shell=True, text=True)
            lines = result.strip().split('\n')
            
            options = []
            for i, line in enumerate(lines):
                parts = line.split('\t')
                if len(parts) == 2:
                    size, path = parts
                    options.append(path)
                    print(f"{i+1}: {Fore.YELLOW}{size}{Style.RESET_ALL} \t {path}")
            
            print(f"{len(lines)+1}: Go Up")
            print(f"{len(lines)+2}: Exit Analyzer")
            
            choice = input(f"Select a directory to drill down [1-{len(lines)+2}]: ")
            
            if not choice.isdigit():
                continue
                
            idx = int(choice)
            if 1 <= idx <= len(lines):
                current_path = options[idx-1]
            elif idx == len(lines) + 1:
                current_path = "/".join(current_path.rstrip("/").split("/")[:-1]) or "/"
            elif idx == len(lines) + 2:
                break
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            break

def systemd_manager(user, host, password):
    while True:
        print(Fore.CYAN + "\n Systemd Service Manager" + Style.RESET_ALL)
        # Fetching running services
        cmd = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {user}@{host} \"systemctl list-units --type=service --state=running --no-pager --no-legend\""
        
        try:
            result = subprocess.check_output(cmd, shell=True, text=True)
            lines = result.strip().split('\n')
            
            services = []
            for i, line in enumerate(lines):
                parts = line.split()
                if len(parts) >= 1:
                    svc_name = parts[0]
                    description = " ".join(parts[4:]) if len(parts) > 4 else ""
                    services.append(svc_name)
                    print(f"{i+1}: {Fore.GREEN}{svc_name:40}{Style.RESET_ALL} {description}")
            
            print(f"{len(services)+1}: Exit Manager")
            choice = input(f"Select a service to manage [1-{len(services)+1}]: ")
            
            if not choice.isdigit():
                continue
            
            idx = int(choice)
            if 1 <= idx <= len(services):
                selected_svc = services[idx-1]
                print(f"\nManaging: {Fore.YELLOW}{selected_svc}{Style.RESET_ALL}")
                print("1: Restart")
                print("2: Stop")
                print("3: Status")
                print("4: Back")
                action_choice = input("Select action [1..4]: ")
                
                action = ""
                if action_choice == "1": action = "restart"
                elif action_choice == "2": action = "stop"
                elif action_choice == "3": action = "status"
                elif action_choice == "4": continue
                
                if action:
                    # Run with sudo
                    exec_cmd = f"sshpass -p '{password}' ssh -tt -o StrictHostKeyChecking=no {user}@{host} \"sudo systemctl {action} {selected_svc}\""
                    subprocess.run(exec_cmd, shell=True)
                    if action == "status":
                        input("\nPress Enter to continue...")
            elif idx == len(services) + 1:
                break
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            break


