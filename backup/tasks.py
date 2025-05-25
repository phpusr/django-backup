import logging

from celery import shared_task

from backup.services import backup_service

logger = logging.getLogger(__name__)


@shared_task
def backup_db_task():
    logger.info('--- Backup DB task started ---')
    result = backup_service.backup_db()

    if not result:
        msg = 'Backup DB task fail or disabled, see logs'
        logger.info(f'>> {msg}')
        return msg

    msg = 'Backup DB task successfully finished'
    logger.info(f'--- {msg} ---')
    return result
