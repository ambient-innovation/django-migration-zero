from django.db import models
from django.utils.translation import gettext_lazy as _


class MigrationZeroConfiguration(models.Model):
    migration_imminent = models.BooleanField(
        _("Migration imminent"),
        default=False,
        help_text=_("Enable this checkbox to prepare the database for a migration zero reset on the next deployment."),
    )
    migration_date = models.DateField(_("Migration date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")

    def __str__(self):
        return "Configuration"
