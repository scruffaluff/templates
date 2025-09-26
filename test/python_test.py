"""Project generation tests."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from test import util

if TYPE_CHECKING:
    from pytest_cookies.plugin import Cookies, Result


TEMPLATE = str(Path(__file__).parents[1] / "python")


@pytest.mark.skipif(
    sys.platform in ["win32"],
    reason="Cookiecutter does not generate files with Windows line endings.",
)
def test_ci(project_python: Result) -> None:
    """Generated project passed ci Just recipe."""
    util.process(
        ["just", "ci"],
        cwd=project_python.project_path,
        env={"CI": "true", "JUST_INIT": "true", **os.environ},
    )


@pytest.mark.parametrize(
    ("context", "paths"),
    [
        (
            {"__project_package": "mock", "project_cli": True},
            ["src/mock/__main__.py"],
        ),
        ({"project_prettier": True}, [".prettierignore", ".prettierrc.yaml"]),
    ],
)
def test_existing_paths(
    context: dict[str, Any], paths: list[str], cookies: Cookies
) -> None:
    """Check that specific paths exist after scaffolding."""
    result = cookies.bake(extra_context=context, template=TEMPLATE)
    assert result.exit_code == 0, str(result.exception)
    for path in paths:
        file_path = result.project_path / path
        assert file_path.exists()


@pytest.mark.parametrize(
    ("context", "paths"),
    [
        (
            {"__project_package": "mock", "project_cli": False},
            ["src/mock/__main__.py"],
        ),
        ({"project_prettier": False}, [".prettierignore", ".prettierrc.yaml"]),
    ],
)
def test_removed_paths(
    context: dict[str, Any], paths: list[str], cookies: Cookies
) -> None:
    """Check that specific paths are removed after scaffolding."""
    result = cookies.bake(extra_context=context, template=TEMPLATE)
    assert result.exit_code == 0, str(result.exception)
    for path in paths:
        remove_path = result.project_path / path
        assert not remove_path.exists()


@pytest.mark.parametrize(
    "context",
    [
        {"project_repository": "https://github.com/scruffaluff/templates"},
        {"project_repository": "https://gitlab.com/scruffaluff/templates"},
        {"project_cli": True},
        {"project_cli": False},
        {"project_prettier": True},
        {"project_prettier": False},
    ],
)
def test_template(context: dict[str, Any], cookies: Cookies) -> None:
    """Check that various configurations generate successfully."""
    result = cookies.bake(extra_context=context, template=TEMPLATE)
    assert result.exit_code == 0, str(result.exception)


@pytest.mark.parametrize(
    ("context", "paths", "text", "exist"),
    [
        (
            {"project_prettier": True},
            ["justfile"],
            "prettier",
            True,
        ),
        (
            {"project_prettier": False},
            ["justfile"],
            "prettier",
            False,
        ),
    ],
)
def test_text_existence(
    context: dict[str, Any],
    paths: list[str],
    text: str,
    exist: bool,
    cookies: Cookies,
) -> None:
    """Check for existence of text in files."""
    result = cookies.bake(extra_context=context, template=TEMPLATE)
    assert result.exit_code == 0, str(result.exception)
    for path in paths:
        text_exists = text in (result.project_path / path).read_text()
        assert text_exists == exist
