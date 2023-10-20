from pathlib import Path
from unittest import mock

from django.test import TestCase

from django_migration_zero.helpers.file_system import (
    build_migration_directory_path,
    delete_file,
    get_local_django_apps,
    get_migration_files,
    has_migration_directory,
)


class HelperFileSystemTest(TestCase):
    # Overriding settings doesn't work for some reason...
    @mock.patch(
        'django_migration_zero.helpers.file_system.MIGRATION_ZERO_APPS_DIR',
        new=Path("/user/workspace/migration_zero/"),
    )
    def test_build_migration_directory_path_regular(self, *args):
        self.assertEqual(
            build_migration_directory_path(app_label='ilyta'), Path('/user/workspace/migration_zero/ilyta/migrations')
        )

    def test_get_local_django_apps_regular(self):
        self.assertEqual(get_local_django_apps(), ['django_migration_zero', 'testapp'])

    def test_has_migration_directory_positive_case(self):
        self.assertTrue(has_migration_directory(app_label="django_migration_zero"))

    def test_has_migration_directory_negative_case(self):
        self.assertFalse(has_migration_directory(app_label="testapp"))

    def test_get_migration_files_regular(self):
        self.assertEqual(get_migration_files(app_label="django_migration_zero"), ['0001_initial.py'])

    def test_get_migration_files_exclude_initials(self):
        self.assertEqual(get_migration_files(app_label="django_migration_zero", exclude_initials=True), [])

    @mock.patch('django_migration_zero.helpers.file_system.os.unlink')
    def test_delete_file_regular(self, mocked_unlink):
        delete_file(app_label='testapp', filename='my_file.py')
        mocked_unlink.assert_called_once()

    @mock.patch('django_migration_zero.helpers.file_system.os.unlink')
    def test_delete_file_dry_run(self, mocked_unlink):
        delete_file(app_label='testapp', filename='my_file.py', dry_run=True)
        mocked_unlink.assert_not_called()

    @mock.patch('django_migration_zero.helpers.file_system.os.unlink', side_effect=OSError)
    def test_delete_file_os_error(self, *args):
        self.assertIsNone(delete_file(app_label='testapp', filename='my_file.py', dry_run=False))
