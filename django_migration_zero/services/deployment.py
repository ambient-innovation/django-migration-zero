from logging import Logger

from django.core.management import call_command
from django.db import transaction
from django.db.migrations.recorder import MigrationRecorder

from django_migration_zero.exceptions import InvalidMigrationTreeError
from django_migration_zero.helpers.logger import get_logger
from django_migration_zero.models import MigrationZeroConfiguration


class DatabasePreparationService:
    """
    Service to prepare the database for an upcoming commit in the CI/CD pipeline.
    """

    logger: Logger

    def __init__(self):
        super().__init__()

        self.logger = get_logger()

    @transaction.atomic
    def process(self):
        self.logger.info("Starting migration zero database adjustments...")

        # Fetch configuration singleton from database
        config_singleton = MigrationZeroConfiguration.objects.fetch_singleton()

        # If we encountered a problem or are not planning to do a migration reset, we are done here
        if not (config_singleton and config_singleton.is_migration_applicable):
            return

        # Reset migration history in database for all apps because there might be dependency issues if we keep the
        # records of the other ones
        self.logger.info("Resetting migration history for all apps...")

        MigrationRecorder.Migration.objects.all().delete()

        # Apply migrations via fake because the database is already up-to-date
        self.logger.info("Populating migration history.")
        call_command("migrate", fake=True)

        # Check if migration tree is valid
        self.logger.info("Checking migration integrity.")
        migrate_check = call_command("migrate", check=True)

        if not migrate_check:
            self.logger.info("All good.")
        else:
            raise InvalidMigrationTreeError(
                'The command "migrate --check" returned a non-zero error code. '
                "Your migration structure seems to be invalid."
            )

        # Process finished, deactivate migration zero switch
        self.logger.info("Deactivating migration zero switch in database.")
        config_singleton.migration_imminent = False
        config_singleton.save()

        self.logger.info("Process successfully finished.")
