from logging import Logger

from django.test import TestCase

from django_migration_zero.helpers.logger import get_logger


class HelperLoggerTest(TestCase):
    def test_get_logger_regular(self):
        self.assertIsInstance(get_logger(), Logger)
