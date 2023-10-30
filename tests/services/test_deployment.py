from logging import Logger
from unittest import mock

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from django_migration_zero.exceptions import InvalidMigrationTreeError
from django_migration_zero.models import MigrationZeroConfiguration
from django_migration_zero.services.deployment import DatabasePreparationService


@freeze_time("2023-06-26")
class DatabasePreparationServiceTest(TestCase):
    config: MigrationZeroConfiguration

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.service = DatabasePreparationService()
        cls.config, _ = MigrationZeroConfiguration.objects.get_or_create()

    def test_init_logger_set(self):
        self.assertIsInstance(self.service.logger, Logger)

    def test_process_regular(self):
        # Setup
        self.config.migration_imminent = True
        self.config.migration_date = timezone.now().date()
        self.config.save()

        # Assertions
        self.assertIsNone(self.service.process())

        self.config.refresh_from_db()
        self.assertFalse(self.config.migration_imminent)

    @mock.patch("django_migration_zero.services.deployment.get_local_django_apps")
    def test_process_case_switch_off(self, mocked_get_local_django_apps):
        self.service.process()

        mocked_get_local_django_apps.assert_not_called()

    @mock.patch("django_migration_zero.services.deployment.call_command", return_value=1)
    def test_process_case_migration_check_failed(self, *args):
        # Setup
        self.config.migration_imminent = True
        self.config.migration_date = timezone.now().date()
        self.config.save()

        # Assertion
        with self.assertRaisesMessage(
            InvalidMigrationTreeError,
            'The command "migrate --check" returned a non-zero error code. '
            'Your migration structure seems to be invalid',
        ):
            self.service.process()

    @mock.patch("django_migration_zero.services.deployment.call_command", return_value=0)
    def test_process_validate_all_commands_are_executed(self, mocked_call_command):
        # Setup
        self.config.migration_imminent = True
        self.config.migration_date = timezone.now().date()
        self.config.save()

        # Testable
        self.service.process()

        # Assertions
        calls = mocked_call_command.call_args_list

        self.assertEqual(mocked_call_command.call_count, 2)

        self.assertEqual(calls[0].args, ("migrate",))
        self.assertEqual(calls[0].kwargs, {'fake': True})

        self.assertEqual(calls[1].args, ("migrate",))
        self.assertEqual(calls[1].kwargs, {'check': True})
