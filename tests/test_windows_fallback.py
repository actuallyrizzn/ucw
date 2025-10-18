import types
import pytest

# Ensure imports work when running from repo root
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parser.windows import WindowsParser


class DummyResult:
    def __init__(self, returncode: int, stdout: str):
        self.returncode = returncode
        self.stdout = stdout


def test_windows_help_fallback(monkeypatch):
    """When /? fails, parser should try /help and return its output."""

    def fake_run(args, capture_output=True, text=True, timeout=10):
        # Simulate failure for primary '/?' and success for '/help'
        if isinstance(args, (list, tuple)) and '/?' in args:
            return DummyResult(returncode=1, stdout='')
        if isinstance(args, (list, tuple)) and '/help' in args:
            return DummyResult(returncode=0, stdout='Usage: dummy [options]')
        return DummyResult(returncode=1, stdout='')

    # Patch both base and windows modules since both call subprocess.run
    import parser.base as base_mod
    import parser.windows as win_mod

    monkeypatch.setattr(base_mod.subprocess, 'run', fake_run)
    monkeypatch.setattr(win_mod.subprocess, 'run', fake_run)

    parser = WindowsParser()
    help_text = parser._get_help_text('dummy')

    assert 'Usage:' in help_text
