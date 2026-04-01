import ui
import connector
import scp_handler
from colorama import Fore, Style
import threading
import time,sys


import glob
import os
import term_mult_client

spinchar = ['|', '/', '-', '\\']

def list_active_sessions():
    sockets = glob.glob("/tmp/velltui_*.sock")
    if not sockets:
        print(Fore.YELLOW + "No active sessions found." + Style.RESET_ALL)
        return None
    
    print(Fore.CYAN + "\n--- Active Persistent Sessions ---" + Style.RESET_ALL)
    for idx, sock in enumerate(sockets, 1):
        host = sock.replace("/tmp/velltui_", "").replace(".sock", "")
        print(f"{idx}: {Fore.GREEN}{host}{Style.RESET_ALL}")
    
    print(f"{len(sockets)+1}: Back to Main Menu")
    choice = input(f"Select session to resume [1-{len(sockets)+1}]: ")
    
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(sockets):
            return sockets[idx-1]
    return None

def simmenu():
    print(Fore.CYAN + "\n Connection Menu... " + Style.RESET_ALL)
    print("1: Connect to existing Profile")
    print("2: Delete an existing Profile")
    print("3: New Connection")
    print("4: Resume Persistent Session")
    print("5: Exit")
    choice = input("Enter your choice: [1/2/3/4/5]: ")

    if choice == "1":
        profile_data = connector.read_profiles()
        if profile_data:
            return profile_data
        return "","",""
    if choice == "2":
        connector.delete_profile()
        return "","",""
    if choice == "3":
        user, host, password = connector.getconn()
        return user, host, password
    if choice == "4":
        return list_active_sessions()
    if choice == "5":
        exit()
    return None

def main():
    ui.print_ban()

    while True:
        conn_data = simmenu()

        if conn_data is None or conn_data == ("","",""):
            continue

        # Check if we are resuming a session (it's a string path)
        if isinstance(conn_data, str):
            term_mult_client.start_client(conn_data)
            continue
        
        # Otherwise, it's a new connection tuple
        user, host, password = conn_data

        result = []
        def ssh_wrapper():
            result.append(connector.test_ssh(user, host, password))

        t1 = threading.Thread(target=ssh_wrapper)
        t1.start()

        i = 0
        while t1.is_alive():
            sys.stdout.write("\r" + "Connecting.... " + spinchar[i % 4])
            sys.stdout.flush()
            time.sleep(0.2)
            i += 1

        sys.stdout.write("\r" + " " * 20 + "\r")
        sys.stdout.flush()

        t1.join()

        if result[0]:
            print(Fore.GREEN + "Connected!" + Style.RESET_ALL)
            while True:
                # We stay in this host's menu until user exits back to main menu
                res = scp_handler.smenu(user, host, password)
                if res == "back": # We'll need to modify smenu to return this
                    break
        else:
            print(Fore.RED + "Connection Failed." + Style.RESET_ALL)

if __name__ == '__main__':
    main()