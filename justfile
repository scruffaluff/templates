# Just configuration file for running commands.
#
# For more information, visit https://just.systems.

mod python
mod vue

set script-interpreter := ["nu"]
set shell := ["nu", "--commands"]
set unstable := true
set windows-shell := ["nu", "--commands"]
export PATH := if os() == "windows" {
  justfile_dir() / ".vendor/bin;" + env("PATH")
} else {
  justfile_dir() / ".vendor/bin:" + env("PATH")
}

# List all commands available in justfile.
list:
  @just --list

# Execute CI workflow commands.
ci: setup lint doc test

# Wrapper to Deno
[no-exit-message]
@deno *args:
  deno {{args}}

# Build documentation.
doc:
  cp python/README.md doc/python.md
  uv tool run --with mkdocs-material,pymdown-extensions mkdocs build --strict

# Fix code formatting.
format:
  deno run --allow-all npm:prettier --write .
  uv run ruff format .

# Run code analyses.
lint: && python::lint vue::lint
  deno run --allow-all npm:prettier --check .
  uv run ruff format --check .

# Install development dependencies.
[script]
setup: _setup
  if (which deno | is-empty) {
    http get https://scruffaluff.github.io/picoware/install/deno.nu
    | nu -c $"($in | decode); main --preserve-env --dest .vendor/bin"
  }
  deno --version
  if (which uv | is-empty) {
    http get https://scruffaluff.github.io/picoware/install/uv.nu
    | nu -c $"($in | decode); main --preserve-env --dest .vendor/bin"
  }
  uv --version

[unix]
_setup:
  #!/usr/bin/env sh
  set -eu
  if [ ! -x "$(command -v nu)" ]; then
    curl --fail --location --show-error \
      https://scruffaluff.github.io/picoware/install/nushell.sh | sh -s -- \
      --preserve-env --dest .vendor/bin
  fi
  echo "Nushell $(nu --version)"

[windows]
_setup:
  #!powershell.exe
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  $PSNativeCommandUseErrorActionPreference = $True
  if (-not (Get-Command -ErrorAction SilentlyContinue nu)) {
    $NushellScript = Invoke-WebRequest -UseBasicParsing -Uri `
      https://scruffaluff.github.io/picoware/install/nushell.ps1
    Invoke-Expression "& { $NushellScript } --preserve-env --dest .vendor/bin"
  }
  Write-Output "Nushell $(nu --version)"

# Run test suites.
test: && python::test vue::test

# Wrapper to Uv.
[no-exit-message]
@uv *args:
  uv {{args}}
