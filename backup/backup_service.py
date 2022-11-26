import json
import logging
import tempfile
from datetime import datetime
from typing import Dict

from django.conf import settings
from django.core import management, signing
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BACKUP_DB_FORMAT = getattr(settings, 'BACKUP_DB_FORMAT', 'json')

logger = logging.getLogger(__name__)

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
    logger.warning('Encoded service account file was not found!')

# Creating GDrive service
scopes = ['https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file(service_account_file_path, scopes=scopes)
service = build('drive', 'v3', credentials=credentials, cache_discovery=False)


def backup_db():
    gdrive_folder_id = getattr(settings, 'GDRIVE_FOLDER_ID', None)
    if not gdrive_folder_id:
        logger.warning('Backup DB is disabled because "GDRIVE_FOLDER_ID" is not set')
        return

    with tempfile.NamedTemporaryFile() as tmp_file:
        management.call_command('dumpdata', indent=2, format=BACKUP_DB_FORMAT, output=tmp_file.name)
        result = _upload_file_to_gdrive(tmp_file.name)

    _delete_old_files()

    return result


def _upload_file_to_gdrive(file_path: str) -> Dict[str, str]:
    now_str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    if not settings.ALLOWED_HOSTS:
        suffix = '-DEV'
    elif settings.ALLOWED_HOSTS == ['testserver']:
        suffix = '-TEST'
    else:
        suffix = '-PROD'

    file_name = f'db_{now_str}{suffix}.{BACKUP_DB_FORMAT}'
    file_metadata = {
        'name': file_name,
        'parents': [settings.GDRIVE_FOLDER_ID]
    }

    media = MediaFileUpload(file_path, resumable=True)
    result = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return result


def _delete_old_files():
    result = service.files().list(
        fields='files(id, name)',
        orderBy='name desc',
        pageSize=1000,
        q=f'"{settings.GDRIVE_FOLDER_ID}" in parents'
    ).execute()

    backup_db_file_number = getattr(settings, 'BACKUP_DB_FILE_NUMBER', 30)
    old_files = result['files'][backup_db_file_number:]
    for file in old_files:
        logger.debug('Deleting file:', file)
        service.files().delete(fileId=file['id']).execute()
