"""{{ cookiecutter.project_name }} testing package."""

from pathlib import Path

import toml

import {{ cookiecutter.__project_package }}

REPO_PATH = Path(__file__).parents[1]


def test_version() -> None:
    """Check that all the version tags are in sync."""
    toml_path = REPO_PATH / "pyproject.toml"
    expected = toml.load(toml_path)["project"]["version"]

    actual = {{ cookiecutter.__project_package }}.__version__
    assert actual == expected
