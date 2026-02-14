# Just configuration file for running commands.
#
# For more information, visit https://just.systems.

set script-interpreter := ["nu"]
set shell := ["nu", "--commands"]
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
lint +paths=".":
  deno run --allow-all npm:prettier --check {{paths}}
  uv run ruff format --check {{paths}}
  uv run ruff check {{paths}}
  uv run ty check {{paths}}

# Wrapper to Nushell.
[no-exit-message]
@nu *args:
  nu {{args}}

# Install development dependencies.
[script]
setup: _setup
  if (which deno | is-empty) {
    print "Installing Deno."
    http get https://scruffaluff.github.io/picoware/install/deno.nu
    | nu -c $"($in | decode); main --preserve-env --dest .vendor/bin"
  }
  print $"Using (deno --version)."
  if (which uv | is-empty) {
    print "Installing Uv."
    http get https://scruffaluff.github.io/picoware/install/uv.nu
    | nu -c $"($in | decode); main --preserve-env --dest .vendor/bin"
  }
  print $"Using (uv --version)."
  print "Installing packages with Uv."
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
    echo 'Installing Nushell'.
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

# Run test suites.
test *args:
  uv run pytest {{args}}

# Wrapper to Uv.
[no-exit-message]
@uv *args:
  uv {{args}}
