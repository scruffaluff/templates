# Contributing

Thank you for your interest in contributing to {{ cookiecutter.project_name }}. This guide will
assist you in setting up a development environment, understanding the project
tooling, and learning the coding guidelines.

## Setup

To setup the development environment, install [Just](https://just.systems). From
the project folder execute `just setup` and you are ready to code.

## Commands

The `justfile` provides the following recipes for development.

| Recipe        | Description                                    |
| ------------- | ---------------------------------------------- |
| `just build`  | Build project for release with Vite            |
| `just ci`     | Run full CI pipeline: setup, lint, test, build |
| `just format` | Format code with Prettier                      |
| `just lint`   | Run Prettier, ESLint, and Vue TypeScript Check |
| `just run`    | Run Vite dev server                            |
| `just setup`  | Install development tools and dependencies     |
| `just test`   | Run unit and end-to-end tests                  |

## Tooling

This project configures the following tools for development usage.

- [ESLint](https://eslint.org): JavaScript and TypeScript linter.
- [Pnpm](https://pnpm.io): Fast, disk space efficient package manager.
- [Playwright](https://playwright.dev): End-to-end testing framework.
- [Prettier](https://prettier.io): Code and configuration file formatter.
- [Vite](https://vitejs.dev): Fast build tool and dev server.
- [Vitest](https://vitest.dev): Next generation testing framework.
- [Vue TypeScript](https://vuejs.org): TypeScript support for Vue.

IDE debugger configurations for VS Code (`.vscode/launch.json`) and Zed
(`.zed/debug.json`) are included.

## Continuous Integration

This project is configured for automated CI on
{%- if cookiecutter.__project_githost == "github" %}GitHub Actions{%- else %}GitLab CI{%- endif %}.

The CI pipeline runs the full `just ci` recipe across Linux, macOS, and Windows
platforms for all code pushes. On Git tag pushes, the pipeline builds artifacts
and publishes a release with package assets. Automated deployment is also
configured to serve the built website from the default branch. The CI pipeline
supports debugging for all jobs with Tmate.
