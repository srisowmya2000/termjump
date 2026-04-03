"""
termjump editor — curses based, works inside zsh widgets on macOS.
"""

import sys
import os
import curses


def tokenize_command(text):
    import re
    tokens = []
    pattern = re.compile(
        r'("(?:[^"\\]|\\.)*")'
        r"|('(?:[^'\\]|\\.)*')"
        r"|(--?[a-zA-Z][a-zA-Z0-9_-]*)"
        r"|([^\s]+)"
    )
    first = True
    for m in pattern.finditer(text):
        s, e = m.start(), m.end()
        tok = m.group(0)
        if m.group(1) or m.group(2):
            cls = "string"
        elif m.group(3):
            cls = "flag"
        elif "/" in tok or tok.endswith((".conf",".json",".yaml",".toml",".sh",".py")):
            cls = "path"
        elif first:
            cls = "cmd"
        else:
            cls = "default"
        tokens.append((s, e, cls))
        first = False
    return tokens


def run_editor(initial_command: str):
    result = {"command": None}

    def _editor(stdscr):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_YELLOW,  -1)
        curses.init_pair(2, curses.COLOR_GREEN,   -1)
        curses.init_pair(3, curses.COLOR_CYAN,    -1)
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)
        curses.init_pair(5, curses.COLOR_WHITE,   -1)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLUE)

        COLOR = {
            "cmd":     curses.color_pair(1) | curses.A_BOLD,
            "flag":    curses.color_pair(2),
            "path":    curses.color_pair(3),
            "string":  curses.color_pair(4),
            "default": curses.color_pair(5),
        }

        curses.curs_set(1)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        stdscr.keypad(True)

        buf = list(initial_command)
        pos = len(buf)

        while True:
            stdscr.clear()
            rows, cols = stdscr.getmaxyx()

            header = "  ● termjump — ENTER confirm  ESC cancel  ^A start  ^E end  click to jump"
            stdscr.attron(curses.color_pair(6))
            stdscr.addstr(0, 0, header[:cols].ljust(cols))
            stdscr.attroff(curses.color_pair(6))

            text = "".join(buf)
            tokens = tokenize_command(text)
            char_color = [COLOR["default"]] * len(text)
            for s, e, cls in tokens:
                for i in range(s, e):
                    char_color[i] = COLOR.get(cls, COLOR["default"])

            stdscr.addstr(1, 0, "  ")
            for i, ch in enumerate(text):
                if 2 + i >= cols - 1:
                    break
                stdscr.addstr(1, 2 + i, ch, char_color[i])

            status = f"  col {pos}/{len(buf)}  |  arrows move  ^A start  ^E end"
            stdscr.attron(curses.color_pair(7))
            stdscr.addstr(2, 0, status[:cols].ljust(cols))
            stdscr.attroff(curses.color_pair(7))

            stdscr.move(1, min(2 + pos, cols - 1))
            stdscr.refresh()

            ch = stdscr.getch()

            if ch in (curses.KEY_ENTER, 10, 13):
                result["command"] = "".join(buf)
                break
            elif ch == 27:
                break
            elif ch == curses.KEY_LEFT and pos > 0:
                pos -= 1
            elif ch == curses.KEY_RIGHT and pos < len(buf):
                pos += 1
            elif ch == 1:
                pos = 0
            elif ch == 5:
                pos = len(buf)
            elif ch in (curses.KEY_BACKSPACE, 127) and pos > 0:
                buf.pop(pos - 1)
                pos -= 1
            elif ch == curses.KEY_DC and pos < len(buf):
                buf.pop(pos)
            elif ch == curses.KEY_MOUSE:
                try:
                    _, mx, my, _, _ = curses.getmouse()
                    if my == 1:
                        pos = min(max(mx - 2, 0), len(buf))
                except curses.error:
                    pass
            elif 32 <= ch <= 126:
                buf.insert(pos, chr(ch))
                pos += 1

    old_stdin  = os.dup(0)
    old_stdout = os.dup(1)
    tty = os.open("/dev/tty", os.O_RDWR)
    os.dup2(tty, 0)
    os.dup2(tty, 1)
    os.close(tty)

    try:
        curses.wrapper(_editor)
    finally:
        os.dup2(old_stdin,  0)
        os.dup2(old_stdout, 1)
        os.close(old_stdin)
        os.close(old_stdout)

    return result["command"]


def main():
    initial = " ".join(sys.argv[1:]) if len(sys.argv) >= 2 else ""
    edited = run_editor(initial)
    if edited is None:
        sys.exit(1)
    sys.stdout.write(edited)
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":
    main()
