"""Reusable testing fixtures."""

from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest
from pytest_cookies.plugin import Cookies, Result


@pytest.fixture(
    params=[
        {"project_cli": True},
        {"project_cli": False},
        {"project_repository": "https://github.com/scruffaluff/templates"},
        {
            "project_repository": "https://gitlab.com/scruffaluff/templates",
            "project_prettier": True,
        },
        {"project_repository": "https://bitbucket.org/scruffaluff/templates"},
        {"project_prettier": True},
        {"project_prettier": False},
    ],
)
def baked_project(cookies: Cookies, request: SubRequest) -> Result:
    """Cookiecutter projects baked from various parameters."""
    return cookies.bake(
        extra_context=request.param, template=str(Path(__file__).parents[1] / "python")
    )
