from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule


class Command(BaseCommand):
    help = 'Create periodic backup tasks'

    def handle(self, *args, **options):
        crontab, created = CrontabSchedule.objects.get_or_create(minute=0, hour=4)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Crontab "{crontab}" created'))
        else:
            self.stdout.write(f'Crontab "{crontab}" already exists')

        task_path = 'backup.tasks.backup_db_task'
        task = PeriodicTask.objects.filter(task=task_path).first()
        exists = task is not None
        if not exists:
            task = PeriodicTask(task=task_path)

        task.crontab = crontab
        task.name = 'backup-db-task'
        task.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Task "{task}" created'))
        else:
            self.stdout.write(f'Task "{task}" updated')
