from django.conf import settings


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

    def backup_db(self):
        pass

    def delete_old_files(self, days: int):
        pass
