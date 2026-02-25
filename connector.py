import subprocess

def getconn():
    user = input("Username: ").strip()
    host = input("Host/IP:  ").strip()
    return user, host

def test_ssh(user, host):
    result = subprocess.run(["ssh", f"{user}@{host}", "exit"])
    return result.returncode == 0

user,host = getconn()
if test_ssh(user,host):
    print("Connection Successful")
else:
    print("Connection Failed")