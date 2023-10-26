from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from django_migration_zero.models import MigrationZeroConfiguration


@freeze_time("2023-09-19")
class MigrationZeroConfigurationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.config, _ = MigrationZeroConfiguration.objects.get_or_create()

    def test_str_regular(self):
        self.assertEqual(str(self.config), "Configuration")

    def test_is_migration_applicable_regular(self):
        # Setup
        self.config.migration_imminent = True
        self.config.migration_date = timezone.now().date()
        self.config.save()

        self.assertTrue(self.config.is_migration_applicable)

    def test_is_migration_applicable_migration_flag_false(self):
        # Setup
        self.config.migration_date = timezone.now().date()
        self.config.save()

        self.assertFalse(self.config.is_migration_applicable)

    def test_is_migration_applicable_migration_date_wrong(self):
        # Setup
        self.config.migration_imminent = True
        self.config.save()

        self.assertFalse(self.config.is_migration_applicable)
