from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from django_migration_zero.services.deployment import DatabasePreparationService


class ManagementCommandHandleMigrationZeroResetTest(TestCase):
    @mock.patch.object(DatabasePreparationService, '__init__', return_value=None)
    @mock.patch.object(DatabasePreparationService, 'process')
    def test_call_parameter_no_parameters(self, mocked_process, mocked_init):
        call_command('handle_migration_zero_reset')
        mocked_init.assert_called_once_with()
