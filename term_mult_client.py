import sys
import socket
import select
import tty
import termios
import os

# Socket Path must match your server's path
socket_path = "/tmp/my_tmux.sock"

def start_client():
    if not os.path.exists(socket_path):
        print(f"Error: Server is not running. (Socket {socket_path} not found)")
        return

    # 1. Connect to the Server
    client_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client_sock.connect(socket_path)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    print("Connected to Multiplexer. (Detaching with Ctrl+C is NOT supported yet, use 'exit' in the terminal)")

    # 2. Set terminal to raw mode
    # This ensures that keys like Ctrl+C are sent to the server, not handled locally.
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        
        while True:
            # 3. Multiplex I/O between Stdin and Socket
            readable, _, _ = select.select([sys.stdin, client_sock], [], [])

            for source in readable:
                if source == sys.stdin:
                    # Data from keyboard -> Send to Server
                    data = os.read(fd, 1024)
                    if not data:
                        break
                    client_sock.sendall(data)

                elif source == client_sock:
                    # Data from Server -> Print to Screen
                    data = client_sock.recv(4096)
                    if not data:
                        # Server closed connection
                        return
                    os.write(sys.stdout.fileno(), data)
                    sys.stdout.flush()

    except Exception as e:
        pass # Handle exit gracefully
    finally:
        # 4. Restore terminal settings on exit
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print("\nDisconnected from Multiplexer.")

if __name__ == "__main__":
    start_client()
