from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import ProgrammingError, models

from django_migration_zero.exceptions import MissingMigrationZeroConfigRecordError
from django_migration_zero.helpers.logger import get_logger


class MigrationZeroConfigurationManager(models.Manager):
    def fetch_singleton(self) -> None:
        logger = get_logger()
        try:
            config_singleton = self.select_for_update().get()
        except ProgrammingError:
            logger.warning(
                "The migration zero table is missing. This might be ok for the first installation of "
                '"django-migration-zero" but if you see this warning after that point, something went sideways.'
            )
            config_singleton = None
        except MultipleObjectsReturned as e:
            raise MissingMigrationZeroConfigRecordError(
                "Too many configuration records detected. There can only be one."
            ) from e
        except ObjectDoesNotExist as e:
            raise MissingMigrationZeroConfigRecordError("No configuration record found in the database.") from e

        return config_singleton
