from logging import Logger
from threading import Thread
from unittest import mock
from unittest.mock import Mock, call

from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from freezegun import freeze_time

from django_migration_zero.exceptions import InvalidMigrationTreeError
from django_migration_zero.managers import MigrationZeroConfigurationQuerySet
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

    @mock.patch.object(MigrationZeroConfiguration, "is_migration_applicable", return_value=False)
    @mock.patch.object(MigrationZeroConfigurationQuerySet, "fetch_singleton", return_value=None)
    def test_process_case_is_migration_applicable_false(self, *args):
        # Setup
        self.config.delete()

        # Assertion
        self.assertIsNone(self.service.process())

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
            "Your migration structure seems to be invalid",
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
        self.assertEqual(calls[0].kwargs, {"fake": True})

        self.assertEqual(calls[1].args, ("migrate",))
        self.assertEqual(calls[1].kwargs, {"check": True})


class DatabasePreparationServiceTestParallelDeployment(TransactionTestCase):
    @mock.patch("django_migration_zero.services.deployment.get_logger")
    def test_process_multiple_threads(self, mock_get_logger):
        """Test parallel deployments to multiple pods."""
        # Setup
        mock_logger_info = Mock(return_value=None)
        mock_get_logger.return_value = Mock(info=mock_logger_info)
        config, _ = MigrationZeroConfiguration.objects.update_or_create(
            defaults={
                "migration_imminent": True,
                "migration_date": timezone.now().date(),
            }
        )

        # Testable
        number_of_pods = 1
        threads = [Thread(target=DatabasePreparationService().process) for _ in range(number_of_pods)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Assertions
        self.assertEqual(mock_logger_info.call_count, 6 + number_of_pods, msg=mock_logger_info.call_args_list)
        mock_logger_info.assert_has_calls(
            [
                call("Starting migration zero database adjustments..."),
                call("Resetting migration history for all apps..."),
                call("Populating migration history."),
                call("Checking migration integrity."),
                call("All good."),
                call("Deactivating migration zero switch in database."),
                call("Process successfully finished."),
            ],
            any_order=True,
        )
        self.assertEqual(
            len(
                [
                    mock_call
                    for mock_call in mock_logger_info.call_args_list
                    if mock_call == call("Starting migration zero database adjustments...")
                ]
            ),
            number_of_pods,
        )

        config.refresh_from_db()
        self.assertFalse(config.migration_imminent)
