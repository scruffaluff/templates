"""Project pre-generation hooks."""

import re
import sys


def name_check(package: str) -> None:
    """Check that the package satisfies JavaScript naming requirements.

    Args:
        package: Importable package name.
    """
    regex = re.compile(r"^[_a-zA-Z][_a-zA-Z0-9-]+$")
    if not regex.match(package):
        print(
            f"ERROR: {package} is not a valid Python importable package name.",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    """Entrypoint for project pre-generation hooks."""
    project_package = "{{ cookiecutter.__project_package }}"
    name_check(project_package)


if __name__ == "__main__":
    main()
