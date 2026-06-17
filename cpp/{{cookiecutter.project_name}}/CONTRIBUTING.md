# Contributing

Thank you for your interest in contributing to {{ cookiecutter.project_name }}. This guide will
assist you in setting up a development environment, understanding the project
tooling, and learning the coding guidelines.

## Setup

To setup the development environment, install [Just](https://just.systems) and a
C++ compiler. From the project folder execute `just setup` and you are ready to
code.

## Commands

The `justfile` provides the following recipes for development.

| Recipe        | Description                                    |
| ------------- | ---------------------------------------------- |
| `just build`  | Build project for release or test              |
| `just ci`     | Run full CI pipeline: setup, lint, test, build |
| `just format` | Format code with Clang Format and Prettier     |
| `just lint`   | Run Prettier, Clang Format, and Clang Tidy     |
{%- if cookiecutter.project_cli %}
| `just run`    | Run project binary (add `DEBUG=1` for LLDB)    |
{%- endif %}
| `just setup`  | Install dev tools and dependencies             |
| `just test`   | Run test suite (add `DEBUG=1` for LLDB)        |

## Tooling

This project configures the following tools for development usage.

- [CMake](https://cmake.org): Cross-platform build system.
- [Clang Format](https://clang.llvm.org/docs/ClangFormat.html): Code formatter.
- [Clang Tidy](https://clang.llvm.org/extra/clang-tidy): Static analyzer.
- [Conan](https://conan.io): C/C++ package manager.
- [Prettier](https://prettier.io): Code formatter for JSON, Markdown, and YAML
  files.

IDE debugger configurations for VS Code (`.vscode/launch.json`) and Zed
(`.zed/debug.json`) are included.

## Continuous Integration

This project is configured for automated CI on
{%- if cookiecutter.__project_githost == "github" %}GitHub Actions{%- else %}GitLab CI{%- endif %}.

The CI pipeline runs the full `just ci` recipe across Linux, macOS, and Windows
platforms for all code pushes. On Git tag pushes, the pipeline builds artifacts
and publishes a release with package assets. The CI pipeline supports debugging
for all jobs with Tmate.
