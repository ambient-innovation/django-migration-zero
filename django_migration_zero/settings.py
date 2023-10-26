from pathlib import Path

from django.conf import settings

from django_migration_zero.exceptions import InvalidMigrationAppsDirPathError


def get_migration_zero_apps_dir() -> Path:
    """
    Helper method to get the settings variable and validate the type
    """
    migration_zero_apps_dir = getattr(settings, "MIGRATION_ZERO_APPS_DIR", Path('/'))

    if not isinstance(migration_zero_apps_dir, Path):
        raise InvalidMigrationAppsDirPathError(
            "Settings variable \"MIGRATION_ZERO_APPS_DIR\" has to be of type pathlib.Path."
        )

    return migration_zero_apps_dir
