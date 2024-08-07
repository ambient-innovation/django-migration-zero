import os
import re
from os.path import isdir
from pathlib import Path

from django.apps import apps
from django.apps.config import AppConfig
from django.conf import settings

from django_migration_zero.helpers.logger import get_logger

logger = get_logger()


def build_migration_directory_path(*, app_path: Path) -> Path:
    """
    Get directory to the migration directory of a given local Django app
    """
    return app_path / "migrations"


def get_local_django_apps() -> list[AppConfig]:
    """
    Iterate all installed Django apps and detect local ones.
    """
    local_apps = []
    local_path = str(settings.BASE_DIR).replace("\\", "/")
    logger.info("Getting local Django apps...")
    for app_config in apps.get_app_configs():
        app_path = str(app_config.path).replace("\\", "/")
        if app_path.startswith(local_path) and "site-packages" not in app_path:
            logger.info(f"Local app {app_config.label!r} discovered.")
            local_apps.append(app_config)
        else:
            logger.debug(f"App {app_config.label!r} ignored since it's not local.")

    return local_apps


def has_migration_directory(*, app_path: Path) -> bool:
    """
    Determines if the given Django app has a migrations directory and therefore migrations
    """
    possible_migration_dir = build_migration_directory_path(app_path=app_path)
    return True if isdir(possible_migration_dir) else False


def get_migration_files(*, app_label: str, app_path: Path, exclude_initials: bool = False) -> list[str]:
    """
    Returns a list of all migration files detected in the given Django app.
    """
    migration_file_list = []

    logger.info(f"Getting migration files from app {app_label!r}...")
    migration_dir = build_migration_directory_path(app_path=app_path)
    file_pattern = r"^\d{4,}_\w+\.py$"
    for filename in os.listdir(migration_dir):
        if re.match(file_pattern, filename):
            if exclude_initials:
                initial_pattern = r"^\d{4,}_initial.py$"
                if re.match(initial_pattern, filename):
                    logger.debug(f"File {filename!r} ignored since it's an initial migration.")
                    continue

            logger.info(f"Migration file {filename!r} detected.")
            migration_file_list.append(filename)
        else:
            logger.debug(f"File {filename!r} ignored since it's not fitting the migration name pattern.")

    return migration_file_list


def delete_file(*, filename: str, app_path: Path, dry_run: bool = False) -> None:
    """
    Physically delete the given file
    """
    file_path = build_migration_directory_path(app_path=app_path) / filename
    if not dry_run:
        try:
            os.unlink(file_path)
            logger.info(f"Deleted file {filename!r}.")
        except OSError:
            logger.warning(f"Unable to delete file {file_path!r}.")
