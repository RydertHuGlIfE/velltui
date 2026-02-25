# SCPCLUI

```
  _____________________________________ .____     ____ ___.___
 /   _____/\_   ___ \______   \_   ___ \|    |   |    |   \   |
 \_____  \ /    \  \/|     ___/    \  \/|    |   |    |   /   |
 /        \\     \___|    |   \     \___|    |___|    |  /|   |
/_______  / \______  /____|    \______  /_______ \______/ |___|
        \/         \/                 \/        \/
```

An interactive command-line interface for SCP (Secure Copy Protocol), built in Python.
Navigate your local and remote filesystems using a TUI file browser and transfer files or entire folders with a single command.

---

## Features

- Interactive TUI file browser for both local and remote paths
- Upload files or folders to a remote server
- Download files or folders from a remote server
- Password entered once and reused for all operations
- Scrollable file list with scrollbar indicator
- Select a destination folder visually without typing paths

---

## Requirements

- Python 3.x
- sshpass

Install sshpass on Arch Linux:
```
sudo pacman -S sshpass
```

---

## Project Structure

```
SCPCLUI/
  main.py         Entry point
  connector.py    SSH connection and credential collection
  scp_handler.py  Menu and SCP command builder
  tuibrow.py      TUI file browser (local and remote)
  ui.py           Banner and display utilities
```

---

## Usage

```
python3 main.py
```

You will be prompted for:
- Remote username
- Remote host or IP address
- Password (hidden input)

Once connected, choose an operation:
1. Upload - select a local file or folder, then select a remote destination folder
2. Download - select a remote file or folder, then select a local destination folder
3. Exit

### TUI Browser Controls

| Key       | Action                        |
|-----------|-------------------------------|
| Up / Down | Navigate the file list        |
| Enter     | Open folder or select file    |
| Enter on [Select this folder] | Use the current directory |
| Q         | Cancel and quit the browser   |

---

## Notes

- Folder transfers use `scp -r` (recursive) automatically
- The password is stored in memory only for the duration of the session
- Remote browsing runs `ls -p` over SSH for each directory you navigate into