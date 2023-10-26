import datetime
from unittest import mock

from django.db import ProgrammingError
from django.test import TestCase

from django_migration_zero.exceptions import MissingMigrationZeroConfigRecordError
from django_migration_zero.models import MigrationZeroConfiguration


class MigrationZeroConfigurationManagerTest(TestCase):
    def test_fetch_singleton_regular(self):
        config = MigrationZeroConfiguration.objects.fetch_singleton()
        self.assertIsInstance(config, MigrationZeroConfiguration)
        self.assertFalse(config.migration_imminent)
        self.assertEqual(config.migration_date, datetime.date(1970, 1, 1))

    def test_fetch_singleton_singleton_exists_via_migration(self):
        self.assertEqual(MigrationZeroConfiguration.objects.all().count(), 1)

    @mock.patch.object(MigrationZeroConfiguration.objects, 'count', side_effect=ProgrammingError)
    def test_fetch_singleton_database_error(self, *args):
        self.assertIsNone(MigrationZeroConfiguration.objects.fetch_singleton())

    def test_fetch_singleton_failure_on_multiple_objects(self):
        MigrationZeroConfiguration.objects.create()

        # Sanity check
        self.assertEqual(MigrationZeroConfiguration.objects.all().count(), 2)

        # Assertion
        with self.assertRaisesMessage(
            MissingMigrationZeroConfigRecordError, "Too many configuration records detected. There can only be one."
        ):
            MigrationZeroConfiguration.objects.fetch_singleton()

    def test_fetch_singleton_failure_on_zero_objects(self):
        # Setup
        MigrationZeroConfiguration.objects.all().delete()

        # Sanity check
        self.assertEqual(MigrationZeroConfiguration.objects.all().count(), 0)

        # Assertion
        with self.assertRaisesMessage(
            MissingMigrationZeroConfigRecordError, "No configuration record found in the database."
        ):
            MigrationZeroConfiguration.objects.fetch_singleton()
