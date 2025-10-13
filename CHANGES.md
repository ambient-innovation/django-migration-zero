# Changelog

**2.3.12** (2025-10-13)
  * Fixed TZ issue for migration date

**2.3.11** (2025-10-10)
  * Maintenance updates via ambient-package-update

**2.3.10** (2025-10-01)
  * Fixed wrong module name in setup docs
  * Fixed missing console handler in setup docs
  * Minor changes via `ambient-package-update`

**2.3.9** (2025-05-29)
  * Maintenance updates via ambient-package-update

**2.3.8** (2025-04-03)
  * Maintenance updates via ambient-package-update

**2.3.7** (2025-02-15)
  * Maintenance updates via ambient-package-update

* *2.3.6* (2024-11-15)
  * Internal updates via `ambient-package-update`

* *2.3.5* (2024-10-14)
  * Added Python 3.13 support
  * Added Djade linter to pre-commit
  * Improved GitHub action triggers
  * Updated dev dependencies and linters

* *2.3.4* (2024-09-11)
  * Added GitHub action trigger for PRs

* *2.3.3* (2024-09-11)
  * Fixed coverage setup due to changes at GitHub

* *2.3.2* (2024-09-11)
  * Fixed package name

* *2.3.1* (2024-08-12)
  * Fixed test matrix

* *2.3.0* (2024-08-12)
  * Added Django 5.1 support

* *2.2.0* (2024-07-18)
  * Use ORM to reset `django_migrations` table
  * Lock rows to enable parallel deployments
  * Dropped Python 3.8 support
  * Added multiple ruff linters and updated packages
  * Updated GitHub actions
  * Added SECURITY.md
  * Internal updates via `ambient-package-update`

* *2.1.0* (2024-07-09)
  * Discover apps in nested directories
  * Use `BASE_DIR` instead of `MIGRATION_ZERO_APPS_DIR`
  * Fixed bug for migrations with > 4 leading digits

* *2.0.3* (2024-06-21)
  * Linted docs with `blacken-docs` via `ambient-package-update`

* *2.0.2* (2024-06-20)
  * Internal updates via `ambient-package-update`

* *2.0.1* (2024-06-14)
  * Internal updates via `ambient-package-update`

* *2.0.0* (2024-04-11)
  * Dropped Django 3.2 & 4.1 support (via `ambient-package-update`)
  * Internal updates via `ambient-package-update`

* *1.1.2* (2023-12-15)
  * Improved documentation

* *1.1.1* (2023-12-06)
  * Improved documentation

* *1.1.0* (2023-12-05)
  * Added Django 5.0 support

* *1.0.6* (2023-11-06)
  * Added "Alternatives" section to docs

* *1.0.5* (2023-11-03)
  * Switched formatter from `black` to `ruff`

* *1.0.4* (2023-10-31)
  * Added `default_auto_field` to app config
  * Linting and test fixes

* *1.0.3* (2023-10-30)
  * Changed django migration table clean-up to delete everything to avoid issue with dependencies

* *1.0.2* (2023-10-27)
  * Set correct min. Django version in requirements
  * Fixed typo in Changelog

* *1.0.1* (2023-10-26)
  * Fixed RTD build

* *1.0.0* (2023-10-26)
  * Official stable release

* *0.1.10* (2023-10-26)
  * Added comprehensive documentation
  * Improved logger warning message

* *0.1.9* (2023-10-24)
  * Reimplemented migration history pruning

* *0.1.8* (2023-10-23)
  * Small improvements

* *0.1.7* (2023-10-23)
  * Migration dir settings improved

* *0.1.6* (2023-10-20)
  * Fixes and adjustments

* *0.1.5* (2023-10-20)
  * Coverage
  * Dependency updates

* *0.1.4* (2023-10-20)
  * Unit-tests

* *0.1.3* (2023-10-20)
  * Improved clean-up command

* *0.1.2* (2023-10-19)
  * Translations, bugfixes and improvements

* *0.1.1* (2023-10-19)
  * Bugfixes and improved logging

* *0.1.0* (2023-10-19)
  * Initial release
