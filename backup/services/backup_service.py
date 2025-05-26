import logging
import tempfile
from datetime import datetime

from django.conf import settings
from django.core import management

BACKUP_DB_FORMAT = getattr(settings, 'BACKUP_DB_FORMAT', 'json')

def get_service():
    backup_type = getattr(settings, 'BACKUP_SERVICE')
    backup_service = None

    if backup_type == 'GOOGLE_DRIVE':
        from backup.services.gdrive_backup_service import GDriveBackupService
        backup_service = GDriveBackupService()
    elif backup_type == 'YANDEX_DISK':
        from backup.services.yadisk_backup_service import YandexDiskBackupService
        backup_service = YandexDiskBackupService()

    if not backup_service:
        raise BackupError(f'Unknown backup service: {backup_type}')

    return backup_service


class BaseBackupService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def backup_db(self):
        with tempfile.NamedTemporaryFile() as tmp_file:
            management.call_command('dumpdata', indent=2, format=BACKUP_DB_FORMAT, output=tmp_file.name)
            now_str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

            if not settings.ALLOWED_HOSTS:
                suffix = '-DEV'
            elif settings.ALLOWED_HOSTS == ['testserver']:
                suffix = '-TEST'
            else:
                suffix = '-PROD'

            upload_filename = f'db_{now_str}{suffix}.{BACKUP_DB_FORMAT}'
            return self.upload_file(tmp_file.name, upload_filename)

    def upload_file(self, filename: str, upload_filename):
        raise NotImplementedError()

    def delete_old_files(self, days: int):
        raise NotImplementedError()


class BackupError(Exception):
    def __init__(self, message):
        self.message = message
