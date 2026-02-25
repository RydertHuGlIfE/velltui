import subprocess
import tuibrow

def smenu(user, host, password):
    print("\nMenu...")
    print("1. Upload")
    print("2. Download")
    print("3. Exit")
    choice = input("Enter your choice: [1/2/3]: ")

    if choice == "1":
        local_path  = tuibrow.browse_local_any()                      # pick file OR folder
        remote_path = tuibrow.browse_remote_folder(user,host,password) # pick dest folder
        cmd = ["sshpass", "-p", password, "scp", "-r", local_path, f"{user}@{host}:{remote_path}"]

    elif choice == "2":
        remote_path = tuibrow.browse_remote_any(user,host,password)   # pick file OR folder
        local_path  = tuibrow.browse_local_folder()                    # pick dest folder
        cmd = ["sshpass", "-p", password, "scp", "-r", f"{user}@{host}:{remote_path}", local_path]

    elif choice == "3":
        exit()

    else:
        print("Invalid choice.")
        return

    subprocess.run(cmd)
