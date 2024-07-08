from pathlib import Path
from unittest import mock

from django.apps import apps
from django.test import TestCase

from django_migration_zero.services.local import ResetMigrationFiles


@mock.patch("django_migration_zero.services.local.delete_file")
class ResetMigrationFilesTest(TestCase):
    def setUp(self):
        self.django_migration_zero_config = apps.get_app_config("django_migration_zero")
        self.testapp_config = apps.get_app_config("testapp")
        self.nested_app_config = apps.get_app_config("nested_app")

    def test_init_regular(self, *args):
        service = ResetMigrationFiles(dry_run=True, exclude_initials=True)

        self.assertTrue(service.dry_run)
        self.assertTrue(service.exclude_initials)

    @mock.patch("django_migration_zero.services.local.has_migration_directory", return_value=True)
    def test_process_case_app_with_migration_found(self, mocked_has_migration_directory, *args):
        service = ResetMigrationFiles()

        with mock.patch(
            "django_migration_zero.services.local.get_local_django_apps",
            return_value=[self.django_migration_zero_config],
        ):
            service.process()

        # Assertion
        mocked_has_migration_directory.assert_called()

    @mock.patch("django_migration_zero.services.local.has_migration_directory", return_value=False)
    def test_process_case_app_with_no_migration_found(self, mocked_has_migration_directory, *args):
        service = ResetMigrationFiles()

        with mock.patch(
            "django_migration_zero.services.local.get_local_django_apps",
            return_value=[self.testapp_config, self.nested_app_config],
        ):
            service.process()

        # Assertion
        mocked_has_migration_directory.assert_called()

    def test_process_delete_file_called(self, mocked_delete_file):
        service = ResetMigrationFiles()
        service.process()

        # Assertion
        mocked_delete_file.assert_called_with(
            filename="0001_initial.py", app_path=Path(self.django_migration_zero_config.path), dry_run=False
        )

    def test_process_delete_file_case_dry_run(self, mocked_delete_file):
        service = ResetMigrationFiles(dry_run=True)
        service.process()

        # Assertion
        mocked_delete_file.assert_called_with(
            filename="0001_initial.py", app_path=Path(self.django_migration_zero_config.path), dry_run=True
        )

    def test_process_delete_file_case_exclude_initials(self, mocked_delete_file):
        service = ResetMigrationFiles(exclude_initials=True)
        service.process()

        # Assertion
        mocked_delete_file.assert_not_called()

    @mock.patch("django_migration_zero.services.local.call_command")
    def test_process_makemigrations_called(self, mocked_call_command, *args):
        service = ResetMigrationFiles()
        service.process()

        # Assertion
        mocked_call_command.assert_called_with("makemigrations")
