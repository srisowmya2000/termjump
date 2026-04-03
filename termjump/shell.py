"""
Generates shell integration scripts for termjump.
"""

ZSH_WIDGET = r"""
# ── termjump zsh integration ─────────────────────────────────────────────────
_termjump_widget() {
  local current_cmd="$BUFFER"
  local tmpfile=$(mktemp /tmp/termjump_XXXXXX)

  # Run in a subshell that has full tty access
  termjump-edit "$current_cmd" > "$tmpfile" 2>/dev/null
  local exit_code=$?

  if [[ $exit_code -eq 0 ]]; then
    local edited=$(cat "$tmpfile")
    if [[ -n "$edited" ]]; then
      BUFFER="$edited"
      CURSOR=${#BUFFER}
    fi
  fi

  rm -f "$tmpfile"
  zle redisplay
}

zle -N _termjump_widget
bindkey '^E' _termjump_widget
# ─────────────────────────────────────────────────────────────────────────────
"""


def print_init_script(shell: str = "zsh") -> None:
    if shell == "zsh":
        print(ZSH_WIDGET)
    else:
        raise ValueError(f"Unsupported shell: {shell}. Currently only zsh is supported.")
