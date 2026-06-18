# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Install

{{ cookiecutter.project_name }} can be installed from source by running the following commands.

```bash
git clone {{ cookiecutter.project_repository }}
cd {{ cookiecutter.project_repository.split("/")[-1] }}
just install
```

## Contribute

For guidance on setting up a development environment and making a contribution
to {{ cookiecutter.project_name }}, see the [contributing guide](CONTRIBUTING.md).
