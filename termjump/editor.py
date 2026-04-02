"""
termjump editor — click any character to jump cursor there.
Built on prompt_toolkit for full terminal/mouse support.
"""

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.mouse_events import MouseEventType
import sys


STYLE = Style.from_dict({
    "status":        "bg:#1a1a2e fg:#7c83fd bold",
    "status.key":    "bg:#1a1a2e fg:#e2e8f0",
    "token.cmd":     "fg:#ffa657 bold",
    "token.flag":    "fg:#3fb950",
    "token.string":  "fg:#d2a8ff",
    "token.path":    "fg:#79c0ff",
    "token.default": "fg:#e6edf3",
    "header":        "bg:#0d1117 fg:#484f58",
})


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
            cls = "token.string"
        elif m.group(3):
            cls = "token.flag"
        elif "/" in tok or tok.endswith((".conf", ".json", ".yaml", ".toml", ".sh", ".py")):
            cls = "token.path"
        elif first:
            cls = "token.cmd"
        else:
            cls = "token.default"
        tokens.append((s, e, cls))
        first = False
    return tokens


def run_editor(initial_command: str) -> str | None:
    result_holder = {"command": None, "cancelled": False}

    from prompt_toolkit.document import Document
    buf = Buffer(
        name="main",
        initial_document=Document(initial_command, cursor_position=len(initial_command)),
        multiline=False,
    )

    kb = KeyBindings()

    @kb.add("enter")
    def accept(event):
        result_holder["command"] = buf.text
        event.app.exit()

    @kb.add("escape")
    @kb.add("c-c")
    def cancel(event):
        result_holder["cancelled"] = True
        event.app.exit()

    @kb.add("c-a")
    def go_home(event):
        buf.cursor_position = 0

    @kb.add("c-e")
    def go_end(event):
        buf.cursor_position = len(buf.text)

    def get_status():
        pos = buf.cursor_position
        total = len(buf.text)
        return HTML(
            f'<status>  termjump </status>'
            f'<status.key>  col <b>{pos}</b>/{total}  </status.key>'
            f'<status.key>  ENTER confirm · ESC cancel · click to jump  </status.key>'
        )

    def mouse_handler(mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            col = mouse_event.position.x
            buf.cursor_position = min(col, len(buf.text))

    layout = Layout(
        HSplit([
            Window(FormattedTextControl(HTML('<header>  ● termjump — smart command editor</header>')), height=1),
            Window(BufferControl(buffer=buf, focusable=True, mouse_handler=mouse_handler), height=1, style="bg:#0d1117 fg:#e6edf3"),
            Window(FormattedTextControl(get_status), height=1),
        ])
    )

    from prompt_toolkit.output.color_depth import ColorDepth
    app = Application(
        layout=layout,
        key_bindings=kb,
        style=STYLE,
        mouse_support=True,
        full_screen=False,
        color_depth=ColorDepth.TRUE_COLOR,
    )
    app.run()

    if result_holder["cancelled"]:
        return None
    return result_holder["command"]


def main():
    initial = " ".join(sys.argv[1:]) if len(sys.argv) >= 2 else ""
    edited = run_editor(initial)
    if edited is None:
        sys.exit(1)
    print(edited, end="")
    sys.exit(0)


if __name__ == "__main__":
    main()
