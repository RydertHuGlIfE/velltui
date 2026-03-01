import subprocess
import sys
import re
from colorama import Fore, Style
import tuibrow

def run_with_progress(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        match = re.search(r'(\d+)%\s+([\d.]+\w+/s)', line)
        if match:
            percent = int(match.group(1))
            speed = match.group(2)
            bar_filled = percent // 2
            bar_empty = 50 - bar_filled
            sys.stdout.write(f"\r[{'█' * bar_filled}{' ' * bar_empty}] {percent}% | {speed}")
            sys.stdout.flush()
    process.wait()
    sys.stdout.write("\r" + " " * 70 + "\r")
    sys.stdout.flush()
    if process.returncode == 0:
        print(Fore.GREEN + "Transfer Complete!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Transfer Failed." + Style.RESET_ALL)

def smenu(user, host, password):
    print("\nMenu...")
    print("1. Upload")
    print("2. Download")
    print("3. Exit")
    choice = input("Enter your choice: [1/2/3]: ")

    if choice == "1":
        local_path  = tuibrow.browse_local_any()
        remote_path = tuibrow.browse_remote_folder(user, host, password)
        cmd = ["rsync", "-avz", "--progress", "-e", f"sshpass -p {password} ssh", local_path, f"{user}@{host}:{remote_path}"]

    elif choice == "2":
        remote_path = tuibrow.browse_remote_any(user, host, password)
        local_path  = tuibrow.browse_local_folder()
        cmd = ["rsync", "-avz", "--progress", "-e", f"sshpass -p {password} ssh", f"{user}@{host}:{remote_path}", local_path]

    elif choice == "3":
        exit()

    else:
        print("Invalid choice.")
        return

    run_with_progress(cmd)
