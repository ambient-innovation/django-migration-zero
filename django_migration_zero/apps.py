from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MigrationZeroConfig(AppConfig):
    name = "migration_zero"
    verbose_name = _("Migration Zero Configuration")
