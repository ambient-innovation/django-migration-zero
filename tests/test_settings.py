from django.conf import settings
from django.test import TestCase, override_settings

from django_migration_zero.exceptions import InvalidMigrationAppsDirPathError
from django_migration_zero.settings import get_migration_zero_apps_dir


class SettingsTest(TestCase):
    def test_get_migration_zero_apps_dir_regular(self):
        self.assertEqual(get_migration_zero_apps_dir(), settings.MIGRATION_ZERO_APPS_DIR)

    @override_settings(MIGRATION_ZERO_APPS_DIR="/usr/path/to/apps")
    def test_get_migration_zero_apps_dir_wrong_type(self):
        with self.assertRaisesMessage(
            InvalidMigrationAppsDirPathError,
            "Settings variable \"MIGRATION_ZERO_APPS_DIR\" has to be of type pathlib.Path.",
        ):
            get_migration_zero_apps_dir()
