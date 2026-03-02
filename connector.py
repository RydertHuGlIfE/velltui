import subprocess
import getpass
from colorama import Fore, Style
import colorama
import json
colorama.init(autoreset=True)

def getconn():
    user     = input(Fore.CYAN + "Username: " + Style.RESET_ALL).strip()
    host     = input(Fore.CYAN + "Host/IP:  " + Style.RESET_ALL).strip()
    password = getpass.getpass(Fore.CYAN + "Password: " + Style.RESET_ALL)
    return user, host, password

def test_ssh(user, host, password):
    result = subprocess.run(
        ["sshpass", "-p", password, "ssh", f"{user}@{host}", "exit"]
    )
    return result.returncode == 0


def read_profiles():
    try:
        with open("profiles.json", "r") as f:
            data = json.load(f)
            profiles = data.get("profiles", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print(Fore.RED + "No profiles found or file is empty." + Style.RESET_ALL)
        return None

    if not profiles:
        print(Fore.YELLOW + "No profiles available." + Style.RESET_ALL)
        return None

    print("\n--- Available Profiles ---")
    for idx, profile in enumerate(profiles, 1):
        print(f"{idx}: {profile['name']} ({profile['user']}@{profile['host']})")

    try:
        choice = int(input("\nSelect profile number: "))
        if 1 <= choice <= len(profiles):
            p = profiles[choice - 1]
            return p["user"], p["host"], p["password"]
        else:
            print(Fore.RED + "Invalid selection." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)

    return None
        

