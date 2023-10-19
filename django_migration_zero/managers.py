from django.db import models

from django_migration_zero.exceptions import MissingMigrationZeroConfigRecordError


class MigrationZeroConfigurationQuerySet(models.QuerySet):
    pass


class MigrationZeroConfigurationManager(models.Manager):
    def fetch_singleton(self) -> None:
        number_records = self.all().count()
        if number_records > 1:
            raise MissingMigrationZeroConfigRecordError(
                "Too many configuration records detected. There can only be one."
            )

        config_singleton = self.all().first()
        if not config_singleton:
            raise MissingMigrationZeroConfigRecordError("No configuration record found in the database.")

        return config_singleton


MigrationZeroConfigurationManager = MigrationZeroConfigurationManager.from_queryset(MigrationZeroConfigurationQuerySet)
