import json
from typing import Dict

from django.conf import settings
from django.core import signing
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from backup.services.backup_service import BaseBackupService


class GDriveBackupService(BaseBackupService):

    def __init__(self):
        super().__init__()

        gdrive_folder_id = getattr(settings, 'GDRIVE_FOLDER_ID', None)
        if not gdrive_folder_id:
            error_msg = 'Backup DB is disabled because "GDRIVE_FOLDER_ID" is not set'
            self.logger.warning(error_msg)
            raise RuntimeError(error_msg)

        # Decoded GDrive service account file
        if hasattr(settings, 'SERVICE_ACCOUNT_FILE_PATH'):
            service_account_file_path = settings.SERVICE_ACCOUNT_FILE_PATH
        else:
            service_account_file_path = settings.BASE_DIR / 'config/gdrive_account.json'

        # Encoded GDrive service account file
        if hasattr(settings, 'ENCODE_SERVICE_ACCOUNT_FILE_PATH'):
            enc_service_account_file_path = settings.ENCODE_SERVICE_ACCOUNT_FILE_PATH
        else:
            enc_service_account_file_path = settings.BASE_DIR / 'config/gdrive_account.enc'

        if enc_service_account_file_path.exists():
            with open(enc_service_account_file_path) as enc_file:
                gdrive_account_data = signing.loads(enc_file.read())

            with open(service_account_file_path, 'w') as service_account_file:
                json.dump(gdrive_account_data, service_account_file, indent=2)
        else:
            self.logger.warning('Encoded service account file was not found!')

        # Creating GDrive service
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(service_account_file_path, scopes=scopes)
        self.service = build('drive', 'v3', credentials=credentials, cache_discovery=False)

    def upload_file(self, file_path: str, upload_filename: str) -> Dict[str, str]:
        file_metadata = {
            'name': upload_filename,
            'parents': [settings.GDRIVE_FOLDER_ID]
        }

        media = MediaFileUpload(file_path, resumable=True)
        return self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    def delete_old_files(self, days_to_keep: int):
        result = self.service.files().list(
            fields='files(id, name)',
            orderBy='name desc',
            pageSize=1000,
            q=f'"{settings.GDRIVE_FOLDER_ID}" in parents'
        ).execute()

        old_files = result['files'][days_to_keep:]
        for file in old_files:
            self.logger.debug('Deleting file:', file)
            self.service.files().delete(fileId=file['id']).execute()
