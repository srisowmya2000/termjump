"""
termjump CLI

  termjump init          → print zsh shell integration snippet
  termjump-edit <cmd>    → open TUI editor, print result to stdout
"""

import sys


def termjump_main():
    """Entry point for the `termjump` command."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print("Usage:")
        print("  termjump init              Print shell integration snippet")
        print("  termjump-edit <command>    Open command editor")
        print()
        print("Quick setup (add to ~/.zshrc):")
        print('  eval "$(termjump init)"')
        sys.exit(0)

    if args[0] == "init":
        from termjump.shell import print_init_script
        print_init_script("zsh")
        sys.exit(0)

    if args[0] == "version":
        from termjump import __version__
        print(f"termjump {__version__}")
        sys.exit(0)

    print(f"Unknown command: {args[0]}", file=sys.stderr)
    sys.exit(1)


def termjump_edit_main():
    """Entry point for `termjump-edit` — opens the TUI editor."""
    from termjump.editor import main
    main()


if __name__ == "__main__":
    termjump_main()
