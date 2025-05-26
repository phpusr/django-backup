import logging

from celery import shared_task

from backup.services.backup_service import get_service

logger = logging.getLogger(__name__)


@shared_task
def backup_db_task():
    logger.info('--- Backup DB task started ---')
    result = get_service().backup_db()

    if not result:
        msg = 'Backup DB task fail or disabled, see logs'
        logger.info(f'>> {msg}')
        return msg

    msg = 'Backup DB task successfully finished'
    logger.info(f'--- {msg} ---')
    return result


@shared_task
def delete_old_db_backups_task(days_to_keep=30):
    logger.info('--- Delete old backups DB task started ---')
    get_service().delete_old_files(days_to_keep)

    msg = 'Delete old backups DB task finished'
    logger.info(f'--- {msg} ---')
