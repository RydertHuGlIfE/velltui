import curses
import os
import subprocess


def browse_local(start_path="/home"):
    return curses.wrapper(_browser_local, start_path, False)

def browse_local_folder(start_path="/home"):
    return curses.wrapper(_browser_local, start_path, True)

def browse_local_any(start_path="/home"):
    return curses.wrapper(_browser_local, start_path, False, True)

def browse_remote(user, host, password, start_path="/home"):
    return curses.wrapper(_browser_remote, user, host, password, start_path, False)

def browse_remote_folder(user, host, password, start_path="/home"):
    return curses.wrapper(_browser_remote, user, host, password, start_path, True)

def browse_remote_any(user, host, password, start_path="/home"):
    return curses.wrapper(_browser_remote, user, host, password, start_path, False, True)
    

def _list_local(path, show_hidden=False):
    items = ["../"]
    try:
        entries = os.listdir(path)
    except PermissionError:
        return items
    
    if not show_hidden:
        entries = [e for e in entries if not e.startswith(".")]
        
    dirs  = sorted([e + "/" for e in entries if os.path.isdir(os.path.join(path, e))])
    files = sorted([e       for e in entries if os.path.isfile(os.path.join(path, e))])
    return items + dirs + files


def _list_remote(user, host, password, path, show_hidden=False):
    # ls -p appends "/" to directories automatically
    ls_cmd = "ls -pa" if show_hidden else "ls -p"
    cmd = ["sshpass", "-p", password, "ssh", f"{user}@{host}", f"{ls_cmd} '{path}'"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip().split("\n")
    out = [e for e in out if e and e not in (".", "..")]
    dirs  = sorted([e for e in out if e.endswith("/")])
    files = sorted([e for e in out if not e.endswith("/")])
    return ["../"] + dirs + files


def _draw(stdscr, items, cursor_pos, title, scroll_offset=0, show_hidden=False):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    visible_rows = h - 2   # rows between title bar and footer

    # Title bar
    try:
        stdscr.addstr(0, 0, f" {title} ".center(w - 1)[:w - 1], curses.A_REVERSE)
    except curses.error:
        pass

    # File list — only draw the visible window
    visible = items[scroll_offset : scroll_offset + visible_rows]
    for row, item in enumerate(visible):
        actual_index = scroll_offset + row
        attr = curses.A_REVERSE if actual_index == cursor_pos else curses.A_NORMAL
        try:
            stdscr.addstr(row + 1, 2, item[:w - 3], attr)
        except curses.error:
            pass

    # Scrollbar indicator
    total = len(items)
    pct = int((cursor_pos / max(total - 1, 1)) * visible_rows)
    try:
        stdscr.addstr(min(pct + 1, h - 2), w - 1, "█")
    except curses.error:
        pass

    # Footer
    h_status = "ON" if show_hidden else "OFF"
    footer = f" ↑↓ Navigate | Enter Open/Select | H Hidden ({h_status}) | Q Quit "
    try:
        stdscr.addstr(h - 1, 0, footer.center(w - 1)[:w - 1], curses.A_REVERSE)
    except curses.error:
        pass

    stdscr.refresh()


# ── Local browser 

def _browser_local(stdscr, start_path, folder_only=False, any_mode=False):
    curses.curs_set(0)
    path = os.path.abspath(start_path)
    cursor_pos = 0
    scroll_offset = 0
    show_hidden = True

    while True:
        base_items = _list_local(path, show_hidden)
        items = (["[\u2713 Select this folder]"] + base_items) if (folder_only or any_mode) else base_items
        h, _ = stdscr.getmaxyx()
        visible_rows = h - 2

        if cursor_pos < scroll_offset:
            scroll_offset = cursor_pos
        elif cursor_pos >= scroll_offset + visible_rows:
            scroll_offset = cursor_pos - visible_rows + 1

        _draw(stdscr, items, cursor_pos, path, scroll_offset, show_hidden)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            cursor_pos = max(0, cursor_pos - 1)
        elif key == curses.KEY_DOWN:
            cursor_pos = min(len(items) - 1, cursor_pos + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            selected = items[cursor_pos]
            if selected == "[\u2713 Select this folder]":
                return path
            elif selected == "../":
                path = os.path.dirname(path)
                cursor_pos = 0
                scroll_offset = 0
            else:
                new_path = os.path.join(path, selected)
                if os.path.isdir(new_path):
                    path = new_path
                    cursor_pos = 0
                    scroll_offset = 0
                elif not folder_only:    # any_mode or normal → pick the file
                    return new_path
        elif key in (ord("h"), ord("H"), ord(".")):
            show_hidden = not show_hidden
            cursor_pos = 0
            scroll_offset = 0
        elif key in (ord("q"), ord("Q")):
            return None


# ── Remote browser 

def _browser_remote(stdscr, user, host, password, start_path, folder_only=False, any_mode=False):
    curses.curs_set(0)
    path = start_path
    cursor_pos = 0
    scroll_offset = 0
    show_hidden = True
    dir_cache = {}   
    while True:
        cache_key = (path, show_hidden)
        if cache_key not in dir_cache:
            dir_cache[cache_key] = _list_remote(user, host, password, path, show_hidden)
        
        items = (["[✓ Select this folder]"] + dir_cache[cache_key]) if (folder_only or any_mode) else dir_cache[cache_key]
        h, _ = stdscr.getmaxyx()
        visible_rows = h - 2

        if cursor_pos < scroll_offset:
            scroll_offset = cursor_pos
        elif cursor_pos >= scroll_offset + visible_rows:
            scroll_offset = cursor_pos - visible_rows + 1

        _draw(stdscr, items, cursor_pos, f"[remote] '{path}'", scroll_offset, show_hidden)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            cursor_pos = max(0, cursor_pos - 1)
        elif key == curses.KEY_DOWN:
            cursor_pos = min(len(items) - 1, cursor_pos + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            selected = items[cursor_pos]
            if selected == "[\u2713 Select this folder]":
                return path
            elif selected == "../":
                path = "/".join(path.rstrip("/").split("/")[:-1]) or "/"
                cursor_pos = 0
                scroll_offset = 0
            elif selected.endswith("/"):
                path = path.rstrip("/") + "/" + selected.rstrip("/")
                cursor_pos = 0
                scroll_offset = 0
            elif not folder_only:    # any_mode or normal → pick the file
                return path.rstrip("/") + "/" + selected
        elif key in (ord("h"), ord("H"), ord(".")):
            show_hidden = not show_hidden
            cursor_pos = 0
            scroll_offset = 0
        elif key in (ord("q"), ord("Q")):
            return None


# ── Test entry point 

if __name__ == "__main__":
    result = browse_local("/home")
    print(f"\nSelected: {result}")