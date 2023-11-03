from ambient_package_update.metadata.author import PackageAuthor
from ambient_package_update.metadata.constants import (
    DEV_DEPENDENCIES,
    LICENSE_MIT,
    SUPPORTED_DJANGO_VERSIONS,
    SUPPORTED_PYTHON_VERSIONS,
)
from ambient_package_update.metadata.package import PackageMetadata
from ambient_package_update.metadata.readme import ReadmeContent

METADATA = PackageMetadata(
    package_name="django_migration_zero",
    authors=[
        PackageAuthor(
            name="Ambient Digital",
            email="hello@ambient.digital",
        ),
    ],
    company="Ambient Innovation: GmbH",
    license=LICENSE_MIT,
    license_year=2023,
    development_status="5 - Production/Stable",
    has_migrations=True,
    readme_content=ReadmeContent(
        tagline="""Welcome to **django-migration-zero** - the holistic implementation of "migration zero" pattern for
Django covering local changes and CI/CD pipeline adjustments.

This package implements the "migration zero" pattern to clean up your local migrations and provides convenient
management commands to recreate your migration files and updating your migration history on your environments
(like test or production systems).""",
        content="""## Features

* Remove all existing local migration files and recreate them as initial migrations
* Configuration singleton in Django admin to prepare your clean-up deployment
* Management command for your pipeline to update Django's migration history table to reflect the changed migrations

## Motivation

Working with any proper ORM will result in database changes which are reflected in migration files to update your
different environment's database structure. These files are versioned in your repository and if you follow any of the
most popular deployment approaches, they won't be needed when they are deployed on production. This means, they clutter
your repo, might lead to merge conflicts in the future and will slow down your test setup.

Django's default way of handling this is called "squashing". This approach is covered broadly in the
[official documentation](https://docs.djangoproject.com/en/dev/topics/migrations/#migration-squashing). The main
drawback here is, that you have to take care of circular dependencies between models. Depending on your project's
size, this can take a fair amount of time.

The main benefit of squashing migrations is, that the history stays intact, therefore it can be used for example in
package which can be installed by anybody and you don't have control over their database.

If you are working on a "regular" application, you have full control over your data(bases) and once everything has
been applied on the "last" system, typically production, the migrations are obsolete. To avoid spending much time on
fixing squashed migrations you won't need, you can use the "migration zero" pattern. In a nutshell, this means:

* Delete all your local migration files
* Recreate initial migration files containing your current model state
* Fix the migration history on every of your environments""",
        additional_installation="""* Add this block to your loggers in your main Django `settings.py` to show
logs in your console.

```python
"django_migration_zero": {
    "handlers": ["console"],
    "level": "INFO",
    "propagate": True,
},
```""",
    ),
    dependencies=[
        "Django>=3.2",
    ],
    supported_django_versions=SUPPORTED_DJANGO_VERSIONS,
    supported_python_versions=SUPPORTED_PYTHON_VERSIONS,
    optional_dependencies={
        "dev": [*DEV_DEPENDENCIES, "unittest-parametrize~=1.3"],
    },
    ruff_ignore_list=[],
)
