"""Project generation tests."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from test import util

if TYPE_CHECKING:
    from pytest_cookies.plugin import Cookies, Result


TEMPLATE = str(Path(__file__).parents[1] / "python")


@pytest.mark.parametrize(
    ("context", "paths"),
    [
        (
            {"project_repository": "https://github.com/scruffaluff/templates"},
            [".github"],
        ),
        (
            {"project_repository": "https://gitlab.com/scruffaluff/templates"},
            [".gitlab-ci.yml"],
        ),
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


def test_mkdocs_build(cookies: Cookies) -> None:
    """Mkdocs must be able to build documentation for baked project."""
    result = cookies.bake(extra_context={}, template=TEMPLATE)
    assert result.exit_code == 0, str(result.exception)
    util.run_command(["uv", "sync"], cwd=result.project_path)
    util.run_command(["just", "doc"], cwd=result.project_path)


def test_mypy_type_checks(project_python: Result) -> None:
    """Generated files must pass Mypy type checks."""
    util.run_command(
        ["uv", "run", "mypy", "."], cwd=project_python.project_path, stream="stdout"
    )


@pytest.mark.skipif(
    sys.platform in ["darwin", "win32"],
    reason="""
    Cookiecutter does not generate files with Windows line endings and Prettier
    returns nonzero exit codes on success for MacOS.
    """,
)
def test_prettier_format(project_python: Result) -> None:
    """Generated files must pass Prettier format checker."""
    if not project_python.context["project_prettier"]:
        pytest.skip("Prettier support is required for format testing.")
    util.run_command(
        [
            "deno",
            "run",
            "--allow-all",
            "npm:prettier",
            "--check",
            ".",
        ],
        cwd=project_python.project_path,
    )


def test_pytest_test(cookies: Cookies) -> None:
    """Generated files must pass Pytest unit tests."""
    result = cookies.bake(extra_context={}, template=TEMPLATE)
    assert result.exit_code == 0, str(result.exception)
    util.run_command(["uv", "sync"], cwd=result.project_path)
    util.run_command(["uv", "run", "pytest"], cwd=result.project_path, stream="stdout")


@pytest.mark.parametrize(
    ("context", "paths"),
    [
        (
            {"project_repository": "https://github.com/scruffaluff/templates"},
            [".gitlab-ci.yml"],
        ),
        (
            {"project_repository": "https://gitlab.com/scruffaluff/templates"},
            [".github"],
        ),
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


def test_ruff_format(project_python: Result) -> None:
    """Generated files must pass Ruff format checker."""
    util.run_command(
        ["uv", "run", "ruff", "format", "--check", "."], cwd=project_python.project_path
    )


def test_ruff_lint(project_python: Result) -> None:
    """Generated files must pass Ruff lints."""
    util.run_command(
        ["uv", "run", "ruff", "check", "."],
        cwd=project_python.project_path,
        stream="stdout",
    )


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
