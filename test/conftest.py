"""Reusable testing fixtures."""

from pathlib import Path

import pytest
from _pytest.fixtures import FixtureRequest
from pytest_cookies.plugin import Cookies, Result

contexts_python = [
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
]
contexts_vue = [
    {"project_repository": "https://github.com/scruffaluff/templates"},
    {"project_repository": "https://gitlab.com/scruffaluff/templates"},
    {"project_repository": "https://bitbucket.org/scruffaluff/templates"},
]
repo_path = Path(__file__).parents[1]


@pytest.fixture(
    params=[
        *(
            {"context": context, "template": repo_path / "python"}
            for context in contexts_python
        ),
        *(
            {"context": context, "template": repo_path / "vue"}
            for context in contexts_vue
        ),
    ],
)
def project(cookies: Cookies, request: FixtureRequest) -> Result:
    """Cookiecutter projects baked from all templates."""
    return cookies.bake(
        extra_context=request.param["context"],
        template=str(request.param["template"]),
    )


@pytest.fixture(params=contexts_python)
def project_python(cookies: Cookies, request: FixtureRequest) -> Result:
    """Cookiecutter projects baked from the python template."""
    return cookies.bake(extra_context=request.param, template=str(repo_path / "python"))


@pytest.fixture(params=contexts_vue)
def project_vue(cookies: Cookies, request: FixtureRequest) -> Result:
    """Cookiecutter projects baked from the vue template."""
    return cookies.bake(extra_context=request.param, template=str(repo_path / "vue"))
