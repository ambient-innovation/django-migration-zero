from ambient_package_update.metadata.author import PackageAuthor
from ambient_package_update.metadata.constants import DEV_DEPENDENCIES, LICENSE_MIT
from ambient_package_update.metadata.package import PackageMetadata
from ambient_package_update.metadata.readme import ReadmeContent
from ambient_package_update.metadata.ruff_ignored_inspection import RuffIgnoredInspection

METADATA = PackageMetadata(
    package_name='django_migration_zero',
    authors=[
        PackageAuthor(
            name='Ambient Digital',
            email='hello@ambient.digital',
        ),
    ],
    company='Ambient Innovation: GmbH',
    license=LICENSE_MIT,
    license_year=2023,
    development_status='5 - Production/Stable',
    readme_content=ReadmeContent(
        tagline="""Welcome to the **django-pony-express** - class-based emails for Django shipping with a full test
suite.

Similar to class-based view in Django core, this package provides a neat, DRY and testable (!) way to handle your
emails in Django.""",
        content="""## Features

* Class-based structure for emails
   * Avoid duplicate low-level setup
   * Utilise inheritance and OOP benefits
   * No duplicated templates for HTML and plain-text
* Test suite to write proper unit-tests for your emails
   * Access your test outbox like a Django queryset

## Etymology

> The Pony Express was an American express mail service that used relays of horse-mounted riders. [...] During its
> 18 months of operation, the Pony Express reduced the time for messages to travel between the east and west US
> coast to about 10 days.
>
> https://en.wikipedia.org/wiki/Pony_Express

The name of this package combines the Django mascot (a pony) with a once quite successful mail service in the US.
Ingenious, right?""",
    ),
    dependencies=[
        'Django>=3.2',
    ],
    optional_dependencies={
        'dev': [
            *DEV_DEPENDENCIES,
        ],
    },
)
