# Template Vue

Template Vue is a repository generator for Vue projects. To create a new Vue
project with the template install
[Cookiecutter](https://github.com/cookiecutter/cookiecutter), execute the
following command, and follow its interactive prompts.

```console
cookiecutter --directory vue gh:scruffaluff/templates
```

## Setup

To develop with the generated project, install [Just](https://just.systems) and
step into the project folder. Then execute `INIT=1 just setup format` and you
are ready to code.

## Continuous Integration

Projects generated with this template repository are automatically configured to
use GitHub CI workflows and GitLab CI pipelines.
