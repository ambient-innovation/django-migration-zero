from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from migration_zero.helpers.logger import get_logger
from migration_zero.managers import MigrationZeroConfigurationManager


class MigrationZeroConfiguration(models.Model):
    migration_imminent = models.BooleanField(
        _("Migration imminent"),
        default=False,
        help_text=_("Enable this checkbox to prepare the database for a migration zero reset on the next deployment."),
    )
    migration_date = models.DateField(_("Migration date"), null=True, blank=True)

    objects = MigrationZeroConfigurationManager()

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")

    def __str__(self):
        return "Configuration"

    @property
    def is_migration_applicable(self) -> bool:
        """
        Checks if we are currently preparing for a "migration zero"-deployment
        """
        logger = get_logger()
        if not self.migration_imminent:
            logger.info("Switch not active. Skipping migration zero process.")
            return False

        if not self.migration_date == timezone.now().date():
            logger.info("Security date doesn't match today. Skipping migration zero process.")
            return False

        return True
