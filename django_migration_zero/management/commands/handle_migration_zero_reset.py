from django.core.management.base import BaseCommand

from django_migration_zero.services.deployment import DatabasePreparationService


class Command(BaseCommand):
    help = "Prepares the database after resetting all migrations."

    def handle(self, *args, **options):
        service = DatabasePreparationService()
        service.process()
