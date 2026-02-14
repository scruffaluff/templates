# Just configuration file for running commands.
#
# For more information, visit https://just.systems.

set script-interpreter := ["nu"]
set shell := ["nu", "--commands"]
set unstable := true
set windows-shell := ["nu", "--commands"]
export PATH := if os() == "windows" {
  justfile_directory() / ".vendor/bin;" + env("PATH")
} else {
  justfile_directory() / ".vendor/bin:" + env("PATH")
}

# List all commands available in justfile.
list:
  @just --list

# Execute CI workflow commands.
ci: setup lint doc test

# Wrapper to Deno.
[no-exit-message]
@deno *args:
  deno {{args}}

# Build documentation.
doc:
  cp python/README.md doc/python.md
  cp vue/README.md doc/vue.md
  uv run mkdocs build --strict

# Fix code formatting.
format +paths=".":
  deno run --allow-all npm:prettier --write {{paths}}
  uv run ruff format {{paths}}

# Run code analyses.
lint:
  deno run --allow-all npm:prettier --check .
  uv run ruff format --check .
  uv run ruff check .
  uv run ty check .

# Wrapper to Nushell.
[no-exit-message]
@nu *args:
  nu {{args}}

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
  if ($env.JUST_INIT? | is-empty) {
    uv sync --locked
  } else {
    uv sync
  }


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
test *args:
  uv run pytest {{args}}

# Wrapper to Uv.
[no-exit-message]
@uv *args:
  uv {{args}}
