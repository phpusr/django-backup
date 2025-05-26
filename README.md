django-backup
=============

A simple Django app to regular backup db to Google Drive.

## Installing

> Insert the [correct version](https://github.com/phpusr/django-backup/tags) instead of the: `v1.1.1`

### Install for Yandex Disk support

```bash
pipenv install git+https://github.com/phpusr/django-backup@v1.1.1#egg=django-backup[yandex-disk]
```

### Install for Google Drive support

```bash
pipenv install git+https://github.com/phpusr/django-backup@v1.1.1#egg=django-backup[gdrive]
```

The app contains a task for [Celery](https://docs.celeryproject.org/) that needs to be registered in your app.

**config/celery.py**

```python
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('app-tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
```

Add `backup` app to settings.py:

**config/settings.py**

```python
INSTALLED_APPS = [
    ...
    'backup',
    'django_celery_beat' # Optional
]

BACKUP_SERVICE = 'YANDEX_DISK' # or 'GOOGLE_DRIVE'

# Backup to Yandex Disk

YANDEX_DISK_TOKEN = os.getenv('YANDEX_DISK_TOKEN')

# Backup to Google Drive

GDRIVE_FOLDER_ID = '1DyhiFFUgmpnwxunHT5yYbqJAw023kjeW'

# Default paths
#SERVICE_ACCOUNT_FILE_PATH = BASE_DIR / 'config/gdrive_account.json'
#ENCODE_SERVICE_ACCOUNT_FILE_PATH = BASE_DIR / 'config/gdrive_account.enc'


# Celery

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost')
```

## How to run

**Normal startup:**

```bash
celery -A backup worker -B -l info
```

**Run with `django-celery-beat`:**

```bash
celery -A backup worker -B --scheduler django -l info
```
