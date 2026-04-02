import sys
import socket
import os
import pty
import select
import signal

signal.signal(signal.SIGHUP, signal.SIG_IGN)

def start_server(user, host, password, socket_path):
    if os.path.exists(socket_path):
        os.remove(socket_path)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)
    server.listen(1)

    print(f"Multiplexer Server started for {host} on {socket_path}")

    master_fd, slave_fd = pty.openpty()
    ssh_pid = os.fork()

    if ssh_pid == 0:
        os.login_tty(slave_fd)
        shell = "zsh" if os.path.exists("/bin/zsh") else "bash"
        os.execvp("sshpass", ["sshpass", "-p", password, "ssh", "-tt",
                               "-o", "StrictHostKeyChecking=no", f"{user}@{host}", shell])
        os._exit(1)

    os.close(slave_fd)

    while True:
        client, _ = server.accept()

        while True:
            try:
                readable, _, _ = select.select([client, master_fd], [], [])
                for source in readable:
                    if source == client:
                        data = client.recv(4096)
                        if not data:
                            client.close()
                            break
                        os.write(master_fd, data)
                    elif source == master_fd:
                        try:
                            output = os.read(master_fd, 4096)
                        except OSError:
                            output = b""
                        if not output:
                            client.close()
                            server.close()
                            os.waitpid(ssh_pid, 0)
                            return
                        client.send(output)
                else:
                    continue
                break
            except (OSError, socket.error):
                client.close()
                break

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: term_mult_server.py <user> <host> <password> <socket_path>")
        sys.exit(1)

    user, host, password, socket_path = sys.argv[1:5]
    start_server(user, host, password, socket_path)