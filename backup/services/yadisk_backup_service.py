import requests
from django.conf import settings

from backup.services.backup_service import BaseBackupService, BackupError

BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'


class YandexDiskBackupService(BaseBackupService):

    def __init__(self):
        super().__init__()
        token = getattr(settings, 'YANDEX_DISK_TOKEN')
        if token is None:
            raise BackupError('Backup DB is disabled because "YANDEX_DISK_TOKEN" is not set')

        self.headers = {
            'Authorization': f'OAuth {token}'
        }

    def upload_file(self, file_path: str, upload_filename: str):
        file_path_on_disk = f'app:/{upload_filename}'
        upload_url = f'{BASE_URL}/upload'

        response = requests.get(upload_url, headers=self.headers, params={
            'path': file_path_on_disk,
            'overwrite': 'true'
        })
        upload_link = response.json().get('href')

        if not upload_link:
            raise BackupError(f'Failed to get upload link')

        with open(file_path, 'rb') as f:
            upload_response = requests.put(upload_link, files={'file': f})

        if upload_response.status_code != 201:
            raise BackupError(f'Failed to upload: {upload_response.text}')

        self.logger.info(f'✅ The file has been successfully uploaded to: %s', file_path_on_disk)
        return upload_response

    def delete_old_files(self, days: int):
        pass
