import logging
import tempfile

from django.conf import settings
from django.core import management

BACKUP_DB_FORMAT = getattr(settings, 'BACKUP_DB_FORMAT', 'json')

def backup_db():
    backup_type = getattr(settings, 'BACKUP_SERVICE')
    backup_service = None

    if backup_type == 'GOOGLE_DRIVE':
        from backup.services.gdrive_backup_service import GDriveBackupService
        backup_service = GDriveBackupService()
    elif backup_type == 'YANDEX_DISK':
        pass

    if backup_service:
        backup_service.backup_db()
        backup_service.delete_old_files(30)


class BaseBackupService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def backup_db(self):
        with tempfile.NamedTemporaryFile() as tmp_file:
            management.call_command('dumpdata', indent=2, format=BACKUP_DB_FORMAT, output=tmp_file.name)
            self.upload_file(tmp_file.name)

    def upload_file(self, filename: str):
        pass

    def delete_old_files(self, days: int):
        pass
