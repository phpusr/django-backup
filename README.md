django-backup
=============

A simple Django app to regular backup db to Google Drive.

## Installing

> Insert the [correct version](https://github.com/phpusr/django-backup/tags) instead of the: `v1.0`

```bash
pipenv install -e git+https://github.com/phpusr/django-backup@v1.0#egg=django-backup
```

The app contains a task for [Celery](https://docs.celeryproject.org/) that needs to be registered in your app.

**config/celery.py**

```python
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('app-tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'backup-db-task': {
        'task': 'backup.tasks.backup_db_task',
        'schedule': crontab(hour=0, minute=0)
    }
}
```

Install `django-celery-beat` (Optional):

```bash
pipenv install django-celery-beat
```

Add `backup` app to settings.py:

**config/settings.py**

```python
INSTALLED_APPS = [
    ...
    'backup',
    'django_celery_beat' # Optional
]

# Backup

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
celery -A backup worker -B -l INFO
```

**Run with `django-celery-beat`:**

```bash
celery -A backup worker -B -l INFO --scheduler django
```
