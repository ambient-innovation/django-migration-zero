from datetime import date

from django.test import TestCase, override_settings
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

    @freeze_time("2023-09-19 10:00:00")
    @override_settings(TIME_ZONE="America/Los_Angeles")
    def test_is_migration_applicable_pacific_timezone(self):
        """Test that migration is applicable when using Pacific timezone"""
        self.config.migration_imminent = True
        self.config.migration_date = date(2023, 9, 19)
        self.config.save()

        self.assertTrue(self.config.is_migration_applicable)

    @freeze_time("2023-09-19 23:00:00")  # 11 PM UTC
    @override_settings(TIME_ZONE="America/New_York")
    def test_is_migration_applicable_eastern_timezone_late_evening(self):
        """
        Test edge case: 11 PM UTC is 7 PM Eastern (same day)
        Migration should be applicable
        """
        self.config.migration_imminent = True
        self.config.migration_date = date(2023, 9, 19)
        self.config.save()

        self.assertTrue(self.config.is_migration_applicable)

    @freeze_time("2023-09-20 02:00:00")  # 2 AM UTC on Sept 20
    @override_settings(TIME_ZONE="America/Los_Angeles")
    def test_is_migration_applicable_pacific_timezone_previous_day(self):
        """
        Test edge case: 2 AM UTC on Sept 20 is 7 PM Pacific on Sept 19
        If migration_date is Sept 19, it should be applicable in Pacific time
        """
        self.config.migration_imminent = True
        self.config.migration_date = date(2023, 9, 19)
        self.config.save()

        self.assertTrue(self.config.is_migration_applicable)

    @freeze_time("2023-09-19 08:00:00")  # 8 AM UTC on Sept 19
    @override_settings(TIME_ZONE="Asia/Tokyo")
    def test_is_migration_applicable_tokyo_timezone_next_day(self):
        """
        Test edge case: 8 AM UTC on Sept 19 is 5 PM Tokyo on Sept 19
        Migration should be applicable for Sept 19
        """
        self.config.migration_imminent = True
        self.config.migration_date = date(2023, 9, 19)
        self.config.save()

        self.assertTrue(self.config.is_migration_applicable)

    @freeze_time("2023-09-19 10:00:00")
    @override_settings(TIME_ZONE="Europe/London")
    def test_is_migration_applicable_london_timezone(self):
        """Test that migration is applicable when using London timezone"""
        self.config.migration_imminent = True
        self.config.migration_date = date(2023, 9, 19)
        self.config.save()

        self.assertTrue(self.config.is_migration_applicable)
