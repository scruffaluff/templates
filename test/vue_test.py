"""Project generation tests."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import pytest

from test import util

if TYPE_CHECKING:
    from pytest_cookies.plugin import Result


@pytest.mark.skipif(
    sys.platform in ["darwin", "win32"],
    reason="""
    Cookiecutter does not generate files with Windows line endings and Prettier
    returns nonzero exit codes on success for MacOS.
    """,
)
def test_lint(project_vue: Result) -> None:
    """Generated files must pass Prettier format checker."""
    util.run_command(
        [
            "just",
            "setup",
            "lint",
        ],
        cwd=project_vue.project_path,
        env={"JUST_INIT": "true", **os.environ},
    )
