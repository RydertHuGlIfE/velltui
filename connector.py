import subprocess
import getpass
from colorama import Fore, Style
import colorama
import json
colorama.init(autoreset=True)

def getconn():
    user = input(Fore.CYAN + "Username: " + Style.RESET_ALL).strip()
    host = input(Fore.CYAN + "Host/IP:  " + Style.RESET_ALL).strip()
    password = getpass.getpass(Fore.CYAN + "Password: " + Style.RESET_ALL)
    return user, host, password

def test_ssh(user, host, password):
    # -o StrictHostKeyChecking=no bypasses the "yes/no" host verification prompt
    result = subprocess.run(
        ["sshpass", "-p", password, "ssh", "-o", "StrictHostKeyChecking=no", f"{user}@{host}", "exit"]
    )
    return result.returncode == 0

def read_profiles():
    try:
        with open("profiles.json", "r") as f:
            data = json.load(f)
            profiles = data.get("profiles", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print(Fore.RED + "No profiles found or file is empty." + Style.RESET_ALL)
        return "","",""

    if not profiles:
        print(Fore.YELLOW + "No profiles available." + Style.RESET_ALL)
        return "","",""

    print("\n--- Available Profiles ---")
    for idx, profile in enumerate(profiles, 1):
        print(f"{idx}: {profile['name']}")

    try:
        print(Fore.YELLOW + "\nSelect profile number: " + Style.RESET_ALL)
        choice = int(input())
        if 1 <= choice <= len(profiles):
            p = profiles[choice - 1]
            return p["user"], p["host"], p["password"]
        else:
            print(Fore.RED + "Invalid selection." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)

    return "","",""

def delete_profile():
    try:
        with open("profiles.json", "r") as f:
            data = json.load(f)
            profiles = data.get("profiles", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print(Fore.RED + "No Profiles found or file is empty" + Style.RESET_ALL)
        return "","",""

    if not profiles:
        print(Fore.YELLOW + "No profiles available" + Style.RESET_ALL)
        return "","","" 

    print("\n--- Available Profiles ---")
    for idx, profile in enumerate(profiles, 1):
        print(f"{idx}: {profile['name']}")

    
    try:
        print(Fore.YELLOW + "\nSelect Profile Number: " + Style.RESET_ALL)
        choice = int(input())
        if 1 <= choice <= len(profiles):
            p = profiles[choice-1]
            profiles.remove(p)
            with open("profiles.json", "w") as f:
                json.dump(data, f, indent=4)
            print(Fore.GREEN + "Profile Deleted Successfully!" + Style.RESET_ALL)
            return "","",""
        else:
            print(Fore.RED + "Invalid selection." + Style.RESET_ALL)
            return "","",""
    except ValueError:
        print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)
        return "","",""

    return "","",""
        

