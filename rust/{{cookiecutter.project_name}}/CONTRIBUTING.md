# Contributing

Thank you for your interest in contributing to {{ cookiecutter.project_name }}. This guide will
assist you in setting up a development environment, understanding the project
tooling, and learning the coding guidelines.

## Setup

To setup the development environment, install [Just](https://just.systems), a C
compiler, and [LLDB](https://lldb.llvm.org) for debugging. From the project
folder execute `just setup` and you are ready to code.

## Commands

The `justfile` provides the following recipes for development.

| Recipe        | Description                                         |
| ------------- | --------------------------------------------------- |
| `just build`  | Build project for release                           |
| `just ci`     | Run full CI pipeline: setup, lint, test, doc, build |
| `just doc`    | Build documentation to `target/doc`                 |
| `just format` | Format code with Rustfmt and Prettier               |
| `just lint`   | Run Prettier, Rustfmt, and Clippy                   |
{%- if cookiecutter.project_cli %}
| `just run`    | Run project binary (add `DEBUG=1` for LLDB)         |
{%- endif %}
| `just setup`  | Install dev tools and dependencies                  |
| `just test`   | Run test suite (add `DEBUG=1` for LLDB)             |

## Tooling

This project configures the following tools for development usage.

- [Cargo](https://doc.rust-lang.org/cargo): Rust package manager and build tool.
- [Clippy](https://doc.rust-lang.org/clippy): Rust linter.
- [Prettier](https://prettier.io): Code formatter for JSON, Markdown, and YAML
  files.
- [Rustfmt](https://github.com/rust-lang/rustfmt): Rust code formatter.
- [Rust Script](https://github.com/fornwall/rust-script): Rust script runner.

IDE debugger configurations for VS Code (`.vscode/launch.json`) and Zed
(`.zed/debug.json`) are included.

## Continuous Integration

This project is configured for automated CI on
{%- if cookiecutter.__project_githost == "github" %}GitHub Actions{%- else %}GitLab CI{%- endif %}.

The CI pipeline runs the full `just ci` recipe across Linux, macOS, and Windows
platforms for all code pushes. On Git tag pushes, the pipeline builds artifacts
and publishes a release with package assets. Automated documentation deployment
is also configured to serve the Rust documentation site from the default branch.
The CI pipeline supports debugging for all jobs with Tmate.
