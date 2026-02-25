import ui
import connector
import scp_handler


def main():
    ui.print_ban()
    user, host, password = connector.getconn()

    if connector.test_ssh(user, host, password):
        print("Connected!")
        scp_handler.smenu(user, host, password)
    else:
        print("Connection Failed.")

if __name__ == '__main__':
    main()