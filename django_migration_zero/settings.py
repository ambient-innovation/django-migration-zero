from pathlib import Path

from django.conf import settings

MIGRATION_ZERO_APPS_DIR = getattr(settings, "MIGRATION_ZERO_APPS_DIR", Path('/'))
