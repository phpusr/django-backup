import json

from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule


class Command(BaseCommand):
    help = 'Create periodic backup tasks'

    def handle(self, *args, **options):
        # noinspection PyUnresolvedReferences
        crontab, created = CrontabSchedule.objects.get_or_create(minute=0, hour=4)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Crontab "{crontab}" created'))
        else:
            self.stdout.write(f'Crontab "{crontab}" already exists')

        # Backup task creating
        self.create_task('backup-db-task', 'backup.tasks.backup_db_task', crontab)

        # Delete old files task creating
        self.create_task('delete-old-db-backups', 'backup.tasks.delete_old_db_backups_task', crontab, {'days_to_keep': 30})

    def create_task(self, name: str, path: str, crontab: CrontabSchedule, kwargs: dict = None):
        task = PeriodicTask.objects.filter(task=path).first()
        exists = task is not None
        if not exists:
            task = PeriodicTask(task=path)

        task.interval = None
        task.crontab = crontab
        task.name = name
        if kwargs:
            task.kwargs = json.dumps(kwargs)
        else:
            task.kwargs = '{}'
        task.save()

        if not exists:
            self.stdout.write(self.style.SUCCESS(f'Task "{task}" created'))
        else:
            self.stdout.write(f'Task "{task}" updated')
