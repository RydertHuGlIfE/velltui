import ui
import connector
import scp_handler
from colorama import Fore, Style
import threading
import time,sys
import socket 
import os 
import pty

socket_path = "/tmp/my_tmux.sock"

if os.path.exists(socket_path):
    os.remove(socket_path)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(socket_path)
server.listen(1)

print("Server started on socket: ", socket_path)

while True:
    client, addr = server.accept()
    print("Client connected: ", addr)
    master_fd, slave_fd = pty.openpty()                      #some virtual terminal or smth 
    pid = os.fork()           #master - server, .... slave-  me also copy the task 


    if pid==0:
        os.login_tty(slave_fd)
        os.execvp("sshpass", ["sshpass", "-p", "password", "ssh", "user@host", "zsh"])
    if pid > 0:
        os.close(slave_fd)           #close slave, let master run 