# Contributing

Thank you for your interest in contributing to {{ cookiecutter.project_name }}. This guide will
assist you in setting up a development environment, understanding the project
tooling, and learning the coding guidelines.

## Setup

To setup the development environment, install [Just](https://just.systems).
From the project folder execute `just setup` and you are ready to code.

## Commands

The `justfile` provides the following recipes for development.

| Recipe            | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `just ci`         | Run full CI pipeline: setup, lint, test, doc, build   |
| `just doc`        | Build MkDocs static site to `build/site`              |
| `just format`     | Format code with Ruff and Prettier                    |
| `just install`    | Build and install the package via pip                 |
| `just lint`       | Run Prettier, Ruff format, Ruff check, and Ty check   |
{%- if cookiecutter.project_cli %}
| `just run`        | Run the CLI entry point (add `DEBUG=1` for pdb)       |
{%- endif %}
| `just setup`      | Install dev tools and sync dependencies               |
| `just test`       | Run Pytest with coverage (add `DEBUG=1` for pdb)      |

Most recipes accept additional arguments. For example, `just test test/foo.py`
runs only that test file, and `just lint src/` lints only the `src` folder.

## Tooling

This project configures the following tools for development usage.

- [Coverage](https://coverage.readthedocs.io/en/coverage-5.0.3): Test coverage
  measurer.
- [MkDocs](https://mkdocs.org): Documentation static site generator.
- [Ruff](https://docs.astral.sh/ruff): Code linter.
- [Pytest](https://docs.pytest.org): Testing framework.
- [Ty](https://docs.astral.sh/ty): Static type checker.
- [Uv](https://docs.astral.sh/uv): Dependency manager and packager.
- [Prettier](https://prettier.io): Opinionated code formatter for JSON,
  Markdown, and YAML files.

IDE debugger configurations for VS Code (`.vscode/launch.json`)
and Zed (`.zed/debug.json`) are included.

## Continuous Integration

This project is configured for automated CI on
{%- if cookiecutter.__project_githost == "github" %}GitHub Actions{%- else %}GitLab CI{%- endif %}.

The CI pipeline runs the full `just ci` recipe across Linux, macOS, and Windows
platforms for all code pushes. On Git tag pushes, the pipeline builds artifacts
and publishes a release with package assets. Automated documentation deployment
is also configured to serve the MkDocs documentation site from the default
branch. The CI pipeline supports debugging for all jobs with Tmate.
