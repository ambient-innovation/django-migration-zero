from pathlib import Path
from unittest import mock

from django.apps import apps
from django.test import TestCase

from django_migration_zero.helpers.file_system import (
    build_migration_directory_path,
    delete_file,
    get_local_django_apps,
    get_migration_files,
    has_migration_directory,
)


class HelperFileSystemTest(TestCase):
    def setUp(self):
        self.django_migration_zero_config = apps.get_app_config("django_migration_zero")
        self.testapp_config = apps.get_app_config("testapp")
        self.nested_app_config = apps.get_app_config("nested_app")

    def test_build_migration_directory_path_regular(self, *args):
        path = Path("/user/workspace/migration_zero/ilyta")
        self.assertEqual(
            build_migration_directory_path(app_path=path), Path("/user/workspace/migration_zero/ilyta/migrations")
        )

    def test_get_local_django_apps_regular(self):
        self.assertEqual(
            get_local_django_apps(),
            [
                self.django_migration_zero_config,
                self.testapp_config,
                self.nested_app_config,
            ],
        )

    def test_has_migration_directory_positive_case(self):
        app_path = Path(self.django_migration_zero_config.path)
        self.assertTrue(has_migration_directory(app_path=app_path))

    def test_has_migration_directory_negative_case(self):
        app_path = Path(self.testapp_config.path)
        self.assertFalse(has_migration_directory(app_path=app_path))

    def test_has_migration_directory_positive_case_no_migrations(self):
        app_path = Path(self.nested_app_config.path)
        self.assertTrue(has_migration_directory(app_path=app_path))

    def test_get_migration_files_regular(self):
        self.assertEqual(
            get_migration_files(
                app_label=self.django_migration_zero_config.label,
                app_path=Path(self.django_migration_zero_config.path),
            ),
            ["0001_initial.py"],
        )

    def test_get_migration_files_exclude_initials(self):
        self.assertEqual(
            get_migration_files(
                app_label=self.django_migration_zero_config.label,
                app_path=Path(self.django_migration_zero_config.path),
                exclude_initials=True,
            ),
            [],
        )

    @mock.patch("django_migration_zero.helpers.file_system.os.unlink")
    def test_delete_file_regular(self, mocked_unlink):
        delete_file(app_path=Path(self.testapp_config.path), filename="my_file.py")
        mocked_unlink.assert_called_once()

    @mock.patch("django_migration_zero.helpers.file_system.os.unlink")
    def test_delete_file_dry_run(self, mocked_unlink):
        delete_file(app_path=Path(self.testapp_config.path), filename="my_file.py", dry_run=True)
        mocked_unlink.assert_not_called()

    @mock.patch("django_migration_zero.helpers.file_system.os.unlink", side_effect=OSError)
    def test_delete_file_os_error(self, *args):
        self.assertIsNone(delete_file(app_path=Path(self.testapp_config.path), filename="my_file.py", dry_run=False))
