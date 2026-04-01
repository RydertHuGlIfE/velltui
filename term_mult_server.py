import ui
import connector
import scp_handler
from colorama import Fore, Style
import threading
import time,sys
import socket 
import os 
import pty
import select

def start_server(user, host, password, socket_path):
    if os.path.exists(socket_path):
        os.remove(socket_path)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)
    server.listen(1)

    print(f"Multiplexer Server started for {host} on {socket_path}")

    while True:
        client, addr = server.accept()
        master_fd, slave_fd = pty.openpty()
        pid = os.fork()

        if pid == 0:
            os.login_tty(slave_fd)
            # Use zsh if available, else bash
            shell = "zsh" if os.path.exists("/bin/zsh") else "bash"
            os.execvp("sshpass", ["sshpass", "-p", password, "ssh", "-tt", "-o", "StrictHostKeyChecking=no", f"{user}@{host}", shell])
        
        if pid > 0:
            os.close(slave_fd)
            while True:
                try:
                    readable, _, _ = select.select([client, master_fd], [], [])
                    for source in readable:
                        if source == client:
                            data = client.recv(4096)
                            if not data: return # Client detached
                            os.write(master_fd, data)
                        elif source == master_fd:
                            output = os.read(master_fd, 4096)
                            if not output: return # SSH session ended
                            client.send(output)
                except (OSError, socket.error):
                    break
            client.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: term_mult_server.py <user> <host> <password> <socket_path>")
        sys.exit(1)
    
    user, host, password, socket_path = sys.argv[1:5]
    start_server(user, host, password, socket_path)

        