"""Smoke-test the installed module and console-script entry points."""

import os
import subprocess
import sys
import sysconfig
from pathlib import Path

from scan2flow import __version__


def test_module_entrypoint():
    result = subprocess.run(
        [sys.executable, "-m", "scan2flow", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == f"scan2flow {__version__}"


def test_installed_console_entrypoint():
    name = "scan2flow.exe" if os.name == "nt" else "scan2flow"
    executable = Path(sysconfig.get_path("scripts")) / name
    assert executable.exists(), "Install with python -m pip install -e '.[dev]' before testing."
    result = subprocess.run(
        [executable, "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == f"scan2flow {__version__}"
