import os
import subprocess
import sys
import re
import json
from colorama import Fore, Style
import tuibrow
import getpass
import extrafet
import time

current_file = "Init..."

def run_with_progress(cmd, password=None):
    # If you use the SSHPASS env var fix, you'll pass password here
    import os
    my_env = os.environ.copy()
    if password:
        my_env["SSHPASS"] = password

    full_output = []
    try:
        # We capture both stdout and stderr (STDOUT) to see the errors
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=my_env)
        
        for line in process.stdout:
            full_output.append(line)  # Save every line to show if it fails
            
            # Progress bar logic
            match = re.search(r'(\d+)%\s+([\d.]+\w+/s)', line)
            if match:
                percent = int(match.group(1))
                speed = match.group(2)
                display_name = current_file[:20] + "..." if len(current_file) > 20 else current_file
                bar_filled = percent // 2
                bar_empty = 50 - bar_filled
                sys.stdout.write(f"\r[{'█' * bar_filled}{' ' * bar_empty}] {percent}% | {speed} | {display_name}")
                sys.stdout.flush()
        
        process.wait()
        sys.stdout.write("\r" + " " * 70 + "\r")
        sys.stdout.flush()

        if process.returncode == 0:
            print(Fore.GREEN + "Transfer Complete!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Transfer Failed." + Style.RESET_ALL)
            print(Fore.YELLOW + "\n--- ACTUAL ERROR FROM RSYNC ---" + Style.RESET_ALL)
            # Print the last few lines of the output to show the error
            print("".join(full_output[-10:])) 
            print(Fore.YELLOW + "-------------------------------" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"\nAn unexpected Python error occurred: {e}" + Style.RESET_ALL)

import term_mult_client

def _probe_socket(path):
    import socket as _s
    try:
        t = _s.socket(_s.AF_UNIX, _s.SOCK_STREAM)
        t.settimeout(2.0)
        t.connect(path)
        t.close()
        return True
    except (ConnectionRefusedError, OSError):
        if os.path.exists(path):
            os.remove(path)
        return False

def _launch_server(user, host, password, socket_path):
    server_dir = os.path.dirname(os.path.abspath(__file__))
    server_args = [sys.executable, os.path.join(server_dir, "term_mult_server.py"),
                   user, host, password, socket_path]
    pid = os.fork()
    if pid == 0:
        os.setsid()
        pid2 = os.fork()
        if pid2 > 0:
            os._exit(0)
        devnull = os.open(os.devnull, os.O_RDWR)
        os.dup2(devnull, 0)
        os.dup2(devnull, 1)
        os.dup2(devnull, 2)
        os.close(devnull)
        os.chdir(server_dir)
        os.execv(sys.executable, server_args)
        os._exit(1)
    os.waitpid(pid, 0)
    time.sleep(1.5)

def persistent_shell(user, host, password):
    # Find all existing sessions for this host
    import glob as _glob
    existing = _glob.glob(f"/tmp/velltui_{host}_*.sock")
    alive = [(p, p.replace(f"/tmp/velltui_{host}_", "").replace(".sock", ""))
             for p in existing if _probe_socket(p)]

    print(Fore.CYAN + f"\n--- Persistent Sessions for {host} ---" + Style.RESET_ALL)
    for i, (path, name) in enumerate(alive, 1):
        print(f"  {i}: {Fore.GREEN}{name}{Style.RESET_ALL} (alive)")
    new_idx = len(alive) + 1
    print(f"  {new_idx}: {Fore.YELLOW}Create New Session{Style.RESET_ALL}")

    choice = input(f"Select [1-{new_idx}]: ").strip()
    if not choice.isdigit():
        return
    idx = int(choice)

    if 1 <= idx <= len(alive):
        # Reconnect to existing session
        term_mult_client.start_client(alive[idx - 1][0])
    elif idx == new_idx:
        name = input("Session name: ").strip().replace(" ", "_") or "default"
        socket_path = f"/tmp/velltui_{host}_{name}.sock"
        if _probe_socket(socket_path):
            print(Fore.YELLOW + "Session already alive, attaching..." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"Starting session '{name}'..." + Style.RESET_ALL)
            _launch_server(user, host, password, socket_path)
        term_mult_client.start_client(socket_path)



def smenu(user, host, password):
    global current_file
    print("\nMenu...")
    print("1. Upload")
    print("2. Download")
    print("3. Add Current Profile")
    print("4. System Monitoring")
    print("5. Remote Shell")
    print("6. Check Server Logs")
    print("7. Basic Server Control")
    print("8. Docker Control")
    print("9: Neo-vim viewer")
    print("10. Disk Usage Analyzer")
    print("11. Systemd Service Manager")
    print("12. Persistent Shell")
    print("13. Back to Main Menu")
    choice = input("Enter your choice: [1..13]: ").strip()

    if choice == "1":
        local_path  = tuibrow.browse_local_any()
        remote_path = tuibrow.browse_remote_folder(user, host, password)
        current_file = os.path.basename(local_path)
        ssh_opts = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
        cmd = ["rsync", "-avz", "-s", "--progress", "-e", f"sshpass -e ssh {ssh_opts}", local_path, f"{user}@{host}:{remote_path}"]

    elif choice == "2":
        remote_path = tuibrow.browse_remote_any(user, host, password)
        local_path  = tuibrow.browse_local_folder()
        current_file = os.path.basename(remote_path)
        ssh_opts = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
        cmd = ["rsync", "-avz", "-s", "--progress", "-e", f"sshpass -e ssh {ssh_opts}", f"{user}@{host}:{remote_path}", local_path]

    elif choice == "3":
        print("Add Current Profile")
        profile_name = input("Enter a name for this profile: ").strip() or f"Profile_{host}"
        new_profile = {
            "name": profile_name,
            "user": user,
            "host": host,
            "password": password
        }
        try:
            with open("profiles.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"profiles": []}

        for profile in data["profiles"]:
            if profile["host"] == host and profile["user"] == user:
                print(Fore.RED + "Profile with this host and user already exists." + Style.RESET_ALL)
                return 

        data["profiles"].append(new_profile)

        with open("profiles.json", "w") as f:
            json.dump(data, f, indent=4)

        
        print(Fore.GREEN + "Profile Added Successfully!" + Style.RESET_ALL)
        return 

    elif choice=="4":
        extrafet.system_monitor(user, host, password)
        return 

    elif choice=="5":
        extrafet.remote_shell(user, host, password)
        return 

    elif choice=="6":
        extrafet.check_logs(user, host, password)
        return 
        
    elif choice == "7":
        extrafet.server_control(user, host, password)
        return 
        
    elif choice == "8":
        extrafet.check_docker_container(user, host, password)
        return
    
    elif choice == "9":
        extrafet.view_files_vim(user, host, password)
        return 

    elif choice == "10":
        extrafet.disk_usage_analyzer(user, host, password)
        return 

    elif choice == "11":
        extrafet.systemd_manager(user, host, password)
        return 

    elif choice == "12":
        persistent_shell(user, host, password)
        return

    elif choice == "13":
        return "back"

    else:
        print("Invalid choice.")
        return

    run_with_progress(cmd, password)
