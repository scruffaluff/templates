"""Reusable testing fixtures."""

from pathlib import Path

import pytest
from _pytest.fixtures import FixtureRequest
from pytest_cookies.plugin import Cookies, Result

contexts_cpp = [
    {
        "project_cli": True,
        "project_repository": "https://github.com/scruffaluff/templates",
    },
]
contexts_python = [
    {
        "project_cli": True,
        "project_repository": "https://github.com/scruffaluff/templates",
    },
    {
        "project_cli": False,
        "project_repository": "https://gitlab.org/scruffaluff/templates",
    },
]
contexts_rust = [
    {
        "project_cli": True,
        "project_repository": "https://github.com/scruffaluff/templates",
    },
    {
        "project_cli": False,
        "project_repository": "https://gitlab.org/scruffaluff/templates",
    },
]
contexts_vue = [
    {"project_repository": "https://github.com/scruffaluff/templates"},
    {"project_repository": "https://gitlab.com/scruffaluff/templates"},
]
repo_path = Path(__file__).parents[1]


@pytest.fixture(
    params=[
        *(
            {"context": context, "template": repo_path / "cpp"}
            for context in contexts_cpp
        ),
        *(
            {"context": context, "template": repo_path / "python"}
            for context in contexts_python
        ),
        *(
            {"context": context, "template": repo_path / "rust"}
            for context in contexts_rust
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


@pytest.fixture(params=contexts_cpp)
def project_cpp(cookies: Cookies, request: FixtureRequest) -> Result:
    """Cookiecutter projects baked from the cpp template."""
    return cookies.bake(extra_context=request.param, template=str(repo_path / "cpp"))


@pytest.fixture(params=contexts_python)
def project_python(cookies: Cookies, request: FixtureRequest) -> Result:
    """Cookiecutter projects baked from the python template."""
    return cookies.bake(extra_context=request.param, template=str(repo_path / "python"))


@pytest.fixture(params=contexts_rust)
def project_rust(cookies: Cookies, request: FixtureRequest) -> Result:
    """Cookiecutter projects baked from the rust template."""
    return cookies.bake(extra_context=request.param, template=str(repo_path / "rust"))


@pytest.fixture(params=contexts_vue)
def project_vue(cookies: Cookies, request: FixtureRequest) -> Result:
    """Cookiecutter projects baked from the vue template."""
    return cookies.bake(extra_context=request.param, template=str(repo_path / "vue"))
