import os
from os.path import isdir
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management import call_command

from migration_zero.settings import MIGRATION_ZERO_APPS_DIR


class ResetMigrationFiles:
    help = "Remove all local migrations files and create new initial ones."

    FILE_WHITELIST = ("__init__.py", "__pycache__")

    dry_run: bool

    def __init__(self, dry_run: bool = False):
        super().__init__()

        self.dry_run = dry_run

    def process(self):
        for app_config in apps.get_app_configs():
            if str(Path(MIGRATION_ZERO_APPS_DIR)) in str(Path(app_config.path)):
                print(f"Detected local app {app_config.label!r}...")

                possible_migration_dir = settings.ROOT_DIR + app_config.label + "migrations"
                if isdir(possible_migration_dir):
                    print("> Migration directory detected...")

                    for filename in os.listdir(possible_migration_dir):
                        if filename not in self.FILE_WHITELIST:
                            print(f">> Removing file {filename!r}.")

                            file_path = possible_migration_dir + filename
                            if not self.dry_run:
                                try:
                                    os.unlink(file_path)
                                except OSError:
                                    print(f"Unable to delete file {file_path!r}.")

        print("\nRecreating new initial migration files...\n")
        call_command("makemigrations")

        print("Process finished.")
