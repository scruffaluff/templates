"""Project generation tests."""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from pytest_cookies.plugin import Cookies


TEMPLATE = str(Path(__file__).parents[1] / "vue")


@pytest.mark.parametrize(
    "context",
    [
        {"project_repository": "https://github.com/scruffaluff/templates"},
        {"project_repository": "https://gitlab.com/scruffaluff/templates"},
    ],
)
def test_badges_separate_lines(context: dict[str, Any], cookies: Cookies) -> None:
    """Readme files must have all badge links on separate lines."""
    result = cookies.bake(extra_context=context, template=TEMPLATE)
    assert result.exit_code == 0, str(result.exception)
    readme = result.project_path / "README.md"

    regex = re.compile(r"img\.shields\.io")
    for line in readme.read_text().split("\n"):
        assert len(regex.findall(line)) < 2  # noqa: PLR2004
