from django.core.management import call_command

from migration_zero.helpers.file_system import (
    delete_file,
    get_local_django_apps,
    get_migration_files,
    has_migration_directory,
)
from migration_zero.helpers.logger import get_logger


class ResetMigrationFiles:
    help = "Remove all local migrations files and create new initial ones."  # noqa: A003

    dry_run: bool

    def __init__(self, dry_run: bool = False):
        super().__init__()

        self.dry_run = dry_run

    def process(self):
        logger = get_logger()
        local_app_list = get_local_django_apps()

        for app_label in local_app_list:
            if not has_migration_directory(app_label=app_label):
                logger.debug(f"Skipping app {app_label!r}. No migration package detected.")
                continue

            migration_file_list = get_migration_files(app_label=app_label)

            for migration_file in migration_file_list:
                delete_file(filename=migration_file, app_label=app_label, dry_run=self.dry_run)

        logger.info("\nRecreating new initial migration files...\n")
        call_command("makemigrations")

        logger.info("Process finished.")
