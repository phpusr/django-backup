import json

from django.conf import settings
from django.core import signing
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        encode_gdrive_account_file()
        self.stdout.write(self.style.SUCCESS('Done'))


def encode_gdrive_account_file():
    if hasattr(settings, 'SERVICE_ACCOUNT_FILE_PATH'):
        service_account_file_path = settings.SERVICE_ACCOUNT_FILE_PATH
    else:
        service_account_file_path = settings.BASE_DIR / 'config/gdrive_account.json'

    if hasattr(settings, 'ENCODE_SERVICE_ACCOUNT_FILE_PATH'):
        enc_service_account_file_path = settings.ENCODE_SERVICE_ACCOUNT_FILE_PATH
    else:
        enc_service_account_file_path = settings.BASE_DIR / 'config/gdrive_account.enc'

    with open(service_account_file_path) as service_account_file:
        with open(enc_service_account_file_path, 'w') as enc_file:
            data = json.load(service_account_file)
            enc_file.write(signing.dumps(data, compress=True))
