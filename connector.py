import subprocess
import getpass

def getconn():
    user     = input("Username: ").strip()
    host     = input("Host/IP:  ").strip()
    password = getpass.getpass("Password: ")
    return user, host, password

def test_ssh(user, host, password):
    result = subprocess.run(
        ["sshpass", "-p", password, "ssh", f"{user}@{host}", "exit"]
    )
    return result.returncode == 0
