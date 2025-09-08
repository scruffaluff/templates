"""Utility functions for testing."""

from __future__ import annotations

import contextlib
import os
import re
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from re import Match
    from subprocess import CompletedProcess

    from pytest_cookies.plugin import Result


@contextlib.contextmanager
def chdir(dest_dir: Path) -> Iterator[None]:
    """Context manager for changing the current working directory.

    Args:
        dest_dir: Directory to temporarily make the current directory.
    """
    # Needs to be called before try statement since current directory can change
    # inside a context manager.
    source_directory = Path.cwd()

    try:
        os.chdir(dest_dir)
        yield
    finally:
        os.chdir(source_directory)


def file_matches(project: Result, regex_str: str) -> Iterator[Path]:
    """Find all files in a directory whose name matches a regex.

    Args:
        project: Directory to search for files.
        regex_str: Regex string for file names to satisfy.

    Yields:
        Matching file paths.
    """
    regex = re.compile(regex_str)
    for path in project.project_path.rglob("*"):
        if path.is_file() and regex.match(path.name):
            yield path


def format_output(process: CompletedProcess) -> str:
    """Format process output for error messages."""
    stdout = f"\n--- STDOUT ---\n{process.stdout.rstrip()}"
    stderr = f"\n--- STDERR ---\n{process.stderr.rstrip()}"
    return f"{stdout}{stderr}\n"


def process(command: Sequence[str], **kwargs: Any) -> CompletedProcess:
    """Wrapper to `subprocess.Popen` with helpful error messages.

    Args:
        command: Command to execute.
        stream: Error message output stream.
        kwargs: Aruments forwarded to `subprocess.Popen`.

    Returns:
        Completed shell process information.
    """
    process = subprocess.run(  # noqa: PLW1510
        command,
        capture_output=True,
        text=True,
        **kwargs,
    )
    assert process.returncode == 0, format_output(process)
    return process


def show(match: Match) -> None:
    """Show lines surrounding regex match.

    Args:
        match: Regex match.
        text: Text parsed by regular expression.
    """
    text = match.string
    start, stop = match.span()

    m = re.match(r"\n.*$", text[:start])
    before = "" if m is None else m.string[m.start() : m.end()]
    m = re.match(r"^.*\n", text[stop:])
    after = "" if m is None else m.string[m.start() : m.end()]

    lines = before + text[start:stop] + after
    print(lines)
