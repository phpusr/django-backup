from django.conf import settings

from backup.services.backup_service import BaseBackupService

BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'


class YandexDiskBackupService(BaseBackupService):

    def __init__(self):
        super().__init__()
        token = getattr(settings, 'YANDEX_DISK_TOKEN')
        if token is None:
            error_msg = 'Backup DB is disabled because "YANDEX_DISK_TOKEN" is not set'
            raise RuntimeError(error_msg)

        self.headers = {
            'Authorization': f'OAuth {token}'
        }

    def delete_old_files(self, days: int):
        pass
