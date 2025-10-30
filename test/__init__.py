"""Tests for template projects."""

from __future__ import annotations

import re
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from test import util

if TYPE_CHECKING:
    from pytest_cookies.plugin import Cookies, Result


templates = ["python", "rust", "vue"]


def test_badges_separate_lines(project: Result) -> None:
    """Readme files must have all badge links on separate lines."""
    readme = project.project_path / "README.md"
    regex = re.compile(r"img\.shields\.io")
    for line in readme.read_text().split("\n"):
        assert len(regex.findall(line)) < 2


@pytest.mark.parametrize(
    ("context", "template", "paths"),
    chain.from_iterable(
        (
            (
                {"project_repository": "https://github.com/scruffaluff/templates"},
                template,
                [".github"],
            ),
            (
                {"project_repository": "https://gitlab.com/scruffaluff/templates"},
                template,
                [".gitlab-ci.yml"],
            ),
        )
        for template in templates
    ),
)
def test_existing_paths(
    context: dict[str, str], template: str, paths: list[str], cookies: Cookies
) -> None:
    """Check that specific paths exist after scaffolding."""
    result = cookies.bake(
        extra_context=context, template=str(Path(__file__).parents[1] / template)
    )
    assert result.exit_code == 0, str(result.exception)
    for path in paths:
        file_path = result.project_path / path
        assert file_path.exists()


def test_no_blank_lines(project: Result) -> None:
    """Project files do not have whitespace only lines."""
    regex = re.compile(r"^\s+$")
    error_msg = "File {}, line {}: {} has whitespace."

    for path in util.file_matches(project, r"^.*$"):
        for idx, line in enumerate(path.read_text().split("\n")):
            match = regex.match(line)
            assert match is None, error_msg.format(path, idx, line)


def test_no_contiguous_blank_lines(project: Result) -> None:
    """Project files do not have subsequent empty lines."""
    regex = re.compile(r"\n\s*\n\s*\n")
    for path in util.file_matches(project, r"^.*(?<!.py)$"):
        text = path.read_text()

        match = regex.search(text)
        assert match is None, f"File {path} has contiguous blank lines."


def test_no_starting_blank_line(project: Result) -> None:
    """Check that generated files do not start with a blank line."""
    regex = re.compile(r"^\s*$")
    for path in util.file_matches(project, r"^.*(?<!\.typed)$"):
        text = path.read_text().split("\n")[0]
        assert not regex.match(text), f"File {path} begins with a blank line."


def test_no_trailing_blank_line(project: Result) -> None:
    """Check that generated files do not have a trailing blank line."""
    regex = re.compile(r"\n\s*$")
    for path in util.file_matches(project, r"^.*$"):
        text = path.read_text()

        match = regex.match(text)
        assert match is None, f"File {path} ends with a blank line."


@pytest.mark.parametrize(
    ("context", "template", "paths"),
    chain.from_iterable(
        (
            (
                {"project_repository": "https://github.com/scruffaluff/templates"},
                template,
                [".gitlab-ci.yml"],
            ),
            (
                {"project_repository": "https://gitlab.com/scruffaluff/templates"},
                template,
                [".github"],
            ),
            (
                {"project_repository": "https://bitbucket.org/scruffaluff/templates"},
                template,
                [".github", ".gitlab-ci.yml"],
            ),
        )
        for template in templates
    ),
)
def test_removed_paths(
    context: dict[str, str], template: str, paths: list[str], cookies: Cookies
) -> None:
    """Check that specific paths are removed after scaffolding."""
    result = cookies.bake(
        extra_context=context, template=str(Path(__file__).parents[1] / template)
    )
    assert result.exit_code == 0, str(result.exception)
    for path in paths:
        remove_path = result.project_path / path
        assert not remove_path.exists()


def test_toml_blank_lines(project: Result) -> None:
    """Check that TOML files do not have blank lines not followed by a [."""
    regex = re.compile(r"\n\s*\n[^[]")
    for path in util.file_matches(project, r"^.*\.toml$"):
        text = path.read_text()
        match = regex.search(text)
        assert match is None, f"TOML file {path} contains blank lines."
