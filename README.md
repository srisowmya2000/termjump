<div align="center">

# ⚡ termjump

### Stop pressing `←` 47 times. Just click.

**A tiny TUI editor that lets you click any character in your terminal command to jump your cursor there instantly.**

[![PyPI version](https://img.shields.io/pypi/v/termjump?color=blueviolet)](https://pypi.org/project/termjump/)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![Shell](https://img.shields.io/badge/shell-zsh-green)](https://www.zsh.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

</div>

---

## 😤 The Problem

Every terminal user knows this pain:
```
$ docker run -it --rm -v /home/user/projects:/workspace -p 8080:8080 myimage:latest
                                         ^^^^^^^^
                                    typo is here 😭
```

Your options?

| Option | Reality |
|--------|---------|
| Press `←` repeatedly | 37 keypresses for one typo |
| `Alt+B` / `Alt+F` | How many words back? Who knows |
| `Ctrl+X Ctrl+E` | Opens full vim. For one character. |
| Retype the whole thing | 😤 |

**There is no way to just click where you want to edit. Until now.**

---

## ✅ The Solution

**termjump** opens a lightweight inline editor right in your terminal.  
Press `Ctrl+E` → the editor pops up → **click any character** → cursor jumps there → fix it → `Enter`.
```
┌──────────────────────────────────────────────────────────────────────┐
│  ● termjump — smart command editor                                   │
│                                                                      │
│  docker run -it --rm -v /home/user/projects:/workspace -p 8080:8080  │
│                                    ^                                 │
│                               click here                             │
│                                                                      │
│  termjump  col 36/72    ENTER confirm · ESC cancel · click to jump   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

**1. Install**
```bash
pip install termjump
```

**2. Add to your `~/.zshrc`**
```zsh
eval "$(termjump init)"
```

**3. Reload your shell**
```bash
source ~/.zshrc
```

**4. Use it**
> Type any command → press `Ctrl+E` → click any character → edit → `Enter`

---

## 🎮 How It Works
```
 You type a command          Press Ctrl+E            Click a character
 ─────────────────           ────────────            ─────────────────

 $ git commit -m            ┌────────────┐           ┌────────────────┐
   "fix autentication"  ──► │  termjump  │  ──────►  │ cursor jumps   │
                            │  editor    │   click!   │ exactly there  │
                            └────────────┘           └────────────────┘
                                                             │
                                                             ▼
                                                      Fix typo → Enter
                                                      Command runs ✓
```

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| 🖱️ **Click** | Jump cursor instantly to any character |
| `←` / `→` | Move one character at a time |
| `Alt+←` / `Alt+→` | Jump one word |
| `Ctrl+A` | Jump to beginning of command |
| `Ctrl+E` | Jump to end of command |
| `Enter` | Confirm and run the command |
| `Esc` / `Ctrl+C` | Cancel — original command stays untouched |

---

## ⚙️ Configuration

**Change the trigger key** (default is `Ctrl+E`):
```zsh
# In your ~/.zshrc, after the eval line:
eval "$(termjump init)"
bindkey '^F' _termjump_widget   # Ctrl+F instead
```

---

## 📋 Requirements

- **Python** 3.10+
- **Shell** — zsh (default on macOS since Catalina)
- **Terminal** with mouse support:
  - ✅ iTerm2
  - ✅ Kitty
  - ✅ WezTerm
  - ✅ macOS Terminal.app

---

## 🤝 Contributing

PRs and issues are very welcome!
```bash
git clone https://github.com/srisowmya2000/termjump
cd termjump
pip install -e ".[dev]"
python tests/test_termjump.py
```

---

<div align="center">
  <br>
  <b>termjump</b> — because arrow keys are not a navigation strategy.
  <br><br>
  Made with 🖱️ for everyone who has ever rage-retyped a long command.
</div>
