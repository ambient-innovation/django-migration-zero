from django.conf import settings
from django.core.management.base import BaseCommand

from django_migration_zero.services.local import ResetMigrationFiles


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Shows affected files without actually deleting them.",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print("Don't run this command in production!")
            return

        service = ResetMigrationFiles(dry_run=options.get("dry_run", False))
        service.process()
