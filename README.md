django-backup
=============

A simple Django app to regular backup db to Google Drive.

The app creates a task for celery that needs to be registered in your app.

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
