[![PyPI release](https://img.shields.io/pypi/v/django-migration-zero.svg)](https://pypi.org/project/django-migration-zero/)
[![Downloads](https://static.pepy.tech/badge/django-migration-zero)](https://pepy.tech/project/django-migration-zero)
[![Linting](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Coding Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Documentation Status](https://readthedocs.org/projects/django-migration-zero/badge/?version=latest)](https://django-migration-zero.readthedocs.io/en/latest/?badge=latest)

Welcome to **django-migration-zero** - the holistic implementation of "migration zero" pattern for
        Django covering local changes and CI/CD pipeline adjustments.

This package implements the "migration zero" pattern to clean up your local migrations and provides convenient
management commands to recreate your migration files and updating your migration history on your environments
(like test or production systems).

* [PyPI](https://pypi.org/project/django-migration-zero/)
* [GitHub](https://github.com/ambient-innovation/django-migration-zero)
* [Full documentation](https://django-migration-zero.readthedocs.io/en/latest/index.html)
* Creator & Maintainer: [Ambient Digital](https://ambient.digital)

## Features

* Remove all existing local migration files and recreate them as initial migrations
* Configuration singleton in Django admin to prepare your clean-up deployment
* Management command for your pipeline to update Django's migration history table to reflect the changed migrations

## Motivation

Working with any proper ORM will result in database changes which are reflected in migration files to update your
different environment's database structure. These files are versioned in your repository and if you follow any of the
most popular deployment approaches, they won't be needed when they are deployed on production. This means, they clutter
your repo, might lead to merge conflicts in the future and will slow down your test setup.

Django's default way of handling this is called "squashing". This approach is covered broadly in the
(official documentation)[https://docs.djangoproject.com/en/dev/topics/migrations/#migration-squashing. The main
drawback here is, that you have to take care of circular dependencies between models. Depending on your project's
size, this can take a fair amount of time.

The main benefit of squashing migrations is, that the history stays intact, therefore it can be used for example in
package which can be installed by anybody and you don't have control over their database.

If you are working on a "regular" application, you have full control over your data(bases) and once everything has
been applied on the "last" system, typically production, the migrations are obsolete. To avoid spending much time on
fixing squashed migrations you won't need, you can use the "migration zero" pattern. In a nutshell, this means:

* Delete all your local migration files
* Recreate initial migration files containing your current model state
* Fix the migration history on every of your environments

## Installation


- Install the package via pip:

  `pip install django-migration-zero`

  or via pipenv:

  `pipenv install django-migration-zero`

- Add module to `INSTALLED_APPS` within the main django `settings.py`:

    ````
    INSTALLED_APPS = (
        ...
        'django_migration_zero',
    )
     ````


## Contribute

### Setup package for development

- Create a Python virtualenv and activate it
- Install "pip-tools" with `pip install pip-tools`
- Compile the requirements with `pip-compile --extra dev, -o requirements.txt pyproject.toml --resolver=backtracking`
- Sync the dependencies with your virtualenv with `pip-sync`

### Add functionality

- Create a new branch for your feature
- Change the dependency in your requirements.txt to a local (editable) one that points to your local file system:
  `-e /Users/workspace/django-migration-zero` or via pip  `pip install -e /Users/workspace/django-migration-zero`
- Ensure the code passes the tests
- Create a pull request

### Run tests

- Run tests
  ````
  pytest --ds settings tests
  ````

### Git hooks (via pre-commit)

We use pre-push hooks to ensure that only linted code reaches our remote repository and pipelines aren't triggered in
vain.

To enable the configured pre-push hooks, you need to [install](https://pre-commit.com/) pre-commit and run once:

    pre-commit install -t pre-push -t pre-commit --install-hooks

This will permanently install the git hooks for both, frontend and backend, in your local
[`.git/hooks`](./.git/hooks) folder.
The hooks are configured in the [`.pre-commit-config.yaml`](templates/.pre-commit-config.yaml.tpl).

You can check whether hooks work as intended using the [run](https://pre-commit.com/#pre-commit-run) command:

    pre-commit run [hook-id] [options]

Example: run single hook

    pre-commit run ruff --all-files --hook-stage push

Example: run all hooks of pre-push stage

    pre-commit run --all-files --hook-stage push

### Update documentation

- To build the documentation run: `sphinx-build docs/ docs/_build/html/`.
- Open `docs/_build/html/index.html` to see the documentation.

### Translation files

If you have added custom text, make sure to wrap it in `_()` where `_` is
gettext_lazy (`from django.utils.translation import gettext_lazy as _`).

How to create translation file:

* Navigate to `django-migration-zero`
* `python manage.py makemessages -l de`
* Have a look at the new/changed files within `django_migration_zero/locale`

How to compile translation files:

* Navigate to `django-migration-zero`
* `python manage.py compilemessages`
* Have a look at the new/changed files within `django_migration_zero/locale`

### Publish to ReadTheDocs.io

- Fetch the latest changes in GitHub mirror and push them
- Trigger new build at ReadTheDocs.io (follow instructions in admin panel at RTD) if the GitHub webhook is not yet set
  up.

### Publish to PyPi

- Update documentation about new/changed functionality

- Update the `Changelog`

- Increment version in main `__init__.py`

- Create pull request / merge to master

- This project uses the flit package to publish to PyPI. Thus publishing should be as easy as running:
  ```
  flit publish
  ```

  To publish to TestPyPI use the following ensure that you have set up your .pypirc as
  shown [here](https://flit.readthedocs.io/en/latest/upload.html#using-pypirc) and use the following command:

  ```
  flit publish --repository testpypi
  ```

### Maintenance

Please note that this package supports the [ambient-package-update](https://pypi.org/project/ambient-package-update/).
So you don't have to worry about the maintenance of this package. All important configuration and setup files are
being rendered by this updater. It works similar to well-known updaters like `pyupgrade` or `django-upgrade`.

To run an update, refer to the [documentation page](https://pypi.org/project/ambient-package-update/)
of the "ambient-package-update".
