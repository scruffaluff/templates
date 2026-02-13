"""Project generation tests."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from test import util

if TYPE_CHECKING:
    from pytest_cookies.plugin import Cookies, Result


TEMPLATE = str(Path(__file__).parents[1] / "vue")


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Cookiecutter does not generate files with Windows line endings.",
)
def test_ci(project_vue: Result) -> None:
    """Generated project passed ci Just recipe."""
    util.process(
        ["just", "ci"],
        cwd=project_vue.project_path,
        env={"CI": "true", "JUST_INIT": "true", **os.environ},
    )


@pytest.mark.parametrize(
    "context",
    [
        {"project_repository": "https://github.com/scruffaluff/templates"},
        {"project_repository": "https://gitlab.com/scruffaluff/templates"},
    ],
)
def test_template(context: dict[str, str], cookies: Cookies) -> None:
    """Check that various configurations generate successfully."""
    result = cookies.bake(extra_context=context, template=TEMPLATE)
    assert result.exit_code == 0, str(result.exception)
