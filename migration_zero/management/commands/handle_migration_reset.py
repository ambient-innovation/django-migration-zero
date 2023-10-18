from os.path import isdir
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from migration_zero.exceptions import InvalidMigrationTreeError, MissingMigrationZeroConfigRecordError
from migration_zero.models import MigrationZeroConfiguration
from migration_zero.settings import MIGRATION_ZERO_APPS_DIR


class Command(BaseCommand):
    help = "Prepares the database after resetting all migrations."  # noqa: A003

    def handle(self, *args, **options):
        print("Starting migration zero database adjustments...")

        # Integrity check
        number_records = MigrationZeroConfiguration.objects.all().count()
        if number_records > 1:
            raise MissingMigrationZeroConfigRecordError(
                "Too many configuration records detected. There can only be one."
            )

        # Fetch configuration singleton from database
        config_singleton: MigrationZeroConfiguration = MigrationZeroConfiguration.objects.all().first()
        if config_singleton:
            print("> Configuration record found.")
        else:
            raise MissingMigrationZeroConfigRecordError("No configuration record found in the database.")

        # If we are not planning to do a migration reset, we are done here
        if not config_singleton.migration_imminent:
            print("Switch not active. Skipping migration zero process.")
            return

        if not config_singleton.migration_date == timezone.now().date():
            print("Security date doesn't match today. Skipping migration zero process.")
            return

        # Reset migration history in database for all local apps
        print("> Resetting migration history for local apps...")
        for app_config in apps.get_app_configs():
            # Local apps have a path which contains the path of the Django app directory
            if str(Path(MIGRATION_ZERO_APPS_DIR)) in str(Path(app_config.path)):
                print(f">> Processing {app_config.label!r}...")

                possible_migration_dir = settings.ROOT_DIR + app_config.label + "migrations"
                if isdir(possible_migration_dir):
                    call_command("migrate", fake=True, app_label=app_config.label, migration_name="zero")

        # Apply migrations via fake because the database is already up-to-date
        print("> Populating migration history.")
        call_command("migrate", fake=True)

        # Check if migration tree is valid
        print("> Checking migration integrity.")
        migrate_check = call_command("migrate", check=True)

        if not migrate_check:
            print(">> All good.")
        else:
            raise InvalidMigrationTreeError(
                'The command "migrate --check" returned a non-zero error code. '
                "Your migration structure seems to be invalid."
            )

        # Process finished, deactivate migration zero switch
        print("> Deactivating migration zero switch in database.")
        config_singleton.migration_imminent = False
        config_singleton.save()

        print("Process successfully finished.")
