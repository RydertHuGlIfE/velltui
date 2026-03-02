import ui
import connector
import scp_handler
from colorama import Fore, Style
import threading
import time,sys


spinchar = ['|', '/', '-', '\\']




def simmenu():
    print("\n Connection Menu... ")
    print("1: Connect to existing Profile: ")
    print("2: New Connection")
    print("3: Exit")
    choice = input("Enter your choice: [1/2/3]: ")

    if choice == "1":
        profile_data = connector.read_profiles()
        if profile_data:
            return profile_data
        return "","",""
    if choice == "2":
        user, host, password = connector.getconn()
        return user, host, password
    if choice == "3":
        exit()
        

def main():
    ui.print_ban()

    conn_data = simmenu()

    if conn_data == ["","",""] or conn_data is None:
        return

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
        scp_handler.smenu(user, host, password)
    else:
        print(Fore.RED + "Connection Failed." + Style.RESET_ALL)

if __name__ == '__main__':
    main()