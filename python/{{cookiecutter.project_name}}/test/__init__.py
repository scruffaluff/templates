"""{{ cookiecutter.project_name }} testing package."""

import tomllib
from pathlib import Path

import {{ cookiecutter.__project_package }}

REPO_PATH = Path(__file__).parents[1]


def test_version() -> None:
    """Check that all the version tags are in sync."""
    path = REPO_PATH / "pyproject.toml"
    with path.open("rb") as file:
        expected = tomllib.load(file)["project"]["version"]

    actual = {{ cookiecutter.__project_package }}.__version__
    assert actual == expected
