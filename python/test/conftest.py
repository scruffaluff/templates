"""Reusable testing fixtures."""

import pytest
from _pytest.fixtures import SubRequest
from pytest_cookies.plugin import Cookies, Result


@pytest.fixture(
    params=[
        {"project_cli": "no"},
        {"project_cli": "yes"},
        {"__project_githost": "github"},
        {"__project_githost": "gitlab", "project_prettier": "no"},
        {"__project_githost": "gitlab"},
        {"project_prettier": "no"},
        {"project_prettier": "yes"},
    ],
)
def baked_project(cookies: Cookies, request: SubRequest) -> Result:
    """Cookiecutter projects baked from various parameters."""
    return cookies.bake(extra_context=request.param)
