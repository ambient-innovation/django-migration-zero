from django.db import ProgrammingError, models

from django_migration_zero.exceptions import MissingMigrationZeroConfigRecordError
from django_migration_zero.helpers.logger import get_logger


class MigrationZeroConfigurationQuerySet(models.QuerySet):
    pass


class MigrationZeroConfigurationManager(models.Manager):
    def fetch_singleton(self) -> None:
        logger = get_logger()
        try:
            number_records = self.count()
        except ProgrammingError:
            logger.warning(
                "The migration table is missing. This might be ok for the first installation of "
                "\"django-migration-zero\" but if you see this warning after that point, something went sideways."
            )
            return None

        if number_records > 1:
            raise MissingMigrationZeroConfigRecordError(
                "Too many configuration records detected. There can only be one."
            )

        config_singleton = self.all().first()
        if not config_singleton:
            raise MissingMigrationZeroConfigRecordError("No configuration record found in the database.")

        return config_singleton


MigrationZeroConfigurationManager = MigrationZeroConfigurationManager.from_queryset(MigrationZeroConfigurationQuerySet)
