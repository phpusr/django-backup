from django.core.management import BaseCommand

from backup.services import backup_service


class Command(BaseCommand):
    def handle(self, *args, **options):
        backup_service.backup_db()
        self.stdout.write(self.style.SUCCESS('Done'))
