# Template C++

Template C++ is a repository generator for C++ projects. To create a new C++
project with the template install
[Cookiecutter](https://github.com/cookiecutter/cookiecutter), execute the
following command, and follow its interactive prompts.

```console
cookiecutter --directory cpp gh:scruffaluff/templates
```

## Setup

To develop with the generated project, install [Just](https://just.systems) and
a C compiler. Then step into the project folder and execute `INIT=1 just setup`
and you are ready to code.

## Continuous Integration

Projects generated with this template repository are automatically configured to
use GitHub CI workflows and GitLab CI pipelines.
