"""
Generates shell integration scripts for termjump.
Usage: termjump init   → prints zsh snippet to eval
"""

ZSH_WIDGET = r"""
# ── termjump zsh integration ─────────────────────────────────────────────────
_termjump_widget() {
  local current_cmd="$BUFFER"

  # Run the editor; capture output
  local edited
  edited=$(termjump-edit "$current_cmd" </dev/tty 2>/dev/tty)
  local exit_code=$?

  if [[ $exit_code -eq 0 && -n "$edited" ]]; then
    BUFFER="$edited"
    CURSOR=${#BUFFER}
  fi

  zle redisplay
}

zle -N _termjump_widget
# Bind to Ctrl+E  (change to taste)
bindkey '^E' _termjump_widget
# ─────────────────────────────────────────────────────────────────────────────
"""


def print_init_script(shell: str = "zsh") -> None:
    if shell == "zsh":
        print(ZSH_WIDGET)
    else:
        raise ValueError(f"Unsupported shell: {shell}. Currently only zsh is supported.")
