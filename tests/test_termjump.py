import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from termjump.editor import tokenize_command
from termjump import __version__

def test_version():
    assert __version__ == "0.1.0"

def test_tokenize_flags():
    tokens = tokenize_command("ls --color -la")
    assert any(c == "token.flag" for _, _, c in tokens)

def test_tokenize_empty():
    assert tokenize_command("") == []

if __name__ == "__main__":
    test_version()
    test_tokenize_flags()
    test_tokenize_empty()
    print("All tests passed ✓")
