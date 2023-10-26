from unittest import mock

from django.core.management import call_command
from django.test import TestCase, override_settings

from django_migration_zero.services.local import ResetMigrationFiles


class ManagementCommandResetLocalMigrationFilesTest(TestCase):
    @override_settings(DEBUG=False)
    @mock.patch.object(ResetMigrationFiles, '__init__')
    def test_debug_barrier(self, mocked_init):
        call_command('reset_local_migration_files')
        mocked_init.assert_not_called()

    @override_settings(DEBUG=True)
    @mock.patch.object(ResetMigrationFiles, '__init__', return_value=None)
    @mock.patch.object(ResetMigrationFiles, 'process')
    def test_call_parameter_no_parameters(self, mocked_process, mocked_init):
        call_command('reset_local_migration_files')
        mocked_init.assert_called_once_with(dry_run=False, exclude_initials=False)

    @override_settings(DEBUG=True)
    @mock.patch.object(ResetMigrationFiles, '__init__', return_value=None)
    @mock.patch.object(ResetMigrationFiles, 'process')
    def test_call_parameter_parameter_dry_run_set(self, mocked_process, mocked_init):
        call_command('reset_local_migration_files', dry_run=True)
        mocked_init.assert_called_once_with(dry_run=True, exclude_initials=False)

    @override_settings(DEBUG=True)
    @mock.patch.object(ResetMigrationFiles, '__init__', return_value=None)
    @mock.patch.object(ResetMigrationFiles, 'process')
    def test_call_parameter_parameter_exclude_initials_set(self, mocked_process, mocked_init):
        call_command('reset_local_migration_files', exclude_initials=True)
        mocked_init.assert_called_once_with(dry_run=False, exclude_initials=True)
