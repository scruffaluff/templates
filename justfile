# Just configuration file for running commands.
#
# For more information, visit https://just.systems.

set script-interpreter := ["nu"]
set shell := ["nu", "--commands"]
export DENO_INSTALL_ROOT := justfile_directory() / ".vendor/lib/deno"
export NO_MKDOCS_2_WARNING := "1"
export PATH := if os() == "windows" {
  justfile_directory() / ".vendor/bin;" + justfile_directory() /
  ".vendor/lib/deno/bin;" + env("PATH")
} else {
  justfile_directory() / ".vendor/bin:" + justfile_directory() /
  ".vendor/lib/deno/bin:" + env("PATH")
}

# Run continuous integration pipeline.
ci: setup lint test doc

# Build documentation.
[script]
doc:
  mkdir doc
  cp README.md doc/index.md
  cp cpp/README.md doc/cpp.md
  cp python/README.md doc/python.md
  cp rust/README.md doc/rust.md
  cp vue/README.md doc/vue.md
  uv run mkdocs build --strict

# Format project files.
format +paths=".":
  prettier --write {{paths}}
  uv run ruff format {{paths}}

# Analyze files for issues.
lint +paths=".":
  prettier --check {{paths}}
  uv run ruff format --check {{paths}}
  uv run ruff check {{paths}}
  uv run ty check {{paths}}

# List available commands.
[default]
@list:
  just --list

# Run Nushell in project environment.
[no-exit-message]
@nu *args="nu --login":
  nu --commands "{{args}}"

# Install development tools and dependencies.
[script]
setup: _setup
  if (which deno | is-empty) {
    print "Installing Deno."
    http get https://scruffaluff.github.io/picoware/install/deno.nu
    | nu -c $"($in | decode); main --preserve-env --dest .vendor/bin"
  }
  print $"Using (deno -V)."
  if (which prettier | is-empty) {
    print "Installing Prettier."
    deno install --allow-all --global npm:prettier
  }
  print $"Using Prettier (prettier --version)."
  if (which uv | is-empty) {
    print "Installing Uv."
    http get https://scruffaluff.github.io/picoware/install/uv.nu
    | nu -c $"($in | decode); main --preserve-env --dest .vendor/bin"
  }
  print $"Using (uv --version)."
  print "Installing packages with Uv."
  if ($env.INIT? | into bool --relaxed) {
    uv sync
    just format
  } else {
    uv sync --locked
  }

[unix]
_setup:
  #!/usr/bin/env sh
  set -eu
  if [ ! -x "$(command -v nu)" ]; then
    echo 'Installing Nushell.'
    curl --fail --location --show-error \
      https://scruffaluff.github.io/picoware/install/nushell.sh | sh -s -- \
      --preserve-env --dest .vendor/bin
  fi
  echo "Using Nushell $(nu --version)."

[windows]
_setup:
  #!powershell.exe
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  $PSNativeCommandUseErrorActionPreference = $True
  if (-not (Get-Command -ErrorAction SilentlyContinue nu)) {
    Write-Output 'Installing Nushell.'
    $NushellScript = Invoke-WebRequest -UseBasicParsing -Uri `
      https://scruffaluff.github.io/picoware/install/nushell.ps1
    Invoke-Expression "& { $NushellScript } --preserve-env --dest .vendor/bin"
  }
  Write-Output "Using Nushell $(nu --version)."

# Run tests (use DEBUG=1 for debugger).
[script]
test *args:
  if ($env.DEBUG? | into bool --relaxed) {
    uv run pytest --pdb {{args}}
  } else {
    uv run pytest {{args}}
  }

# Run Uv in project environment.
[no-exit-message]
@uv *args:
  uv {{args}}
