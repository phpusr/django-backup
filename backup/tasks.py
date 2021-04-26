import logging

from backup import backup_service
from config.celery import app

logger = logging.getLogger(__name__)


@app.task
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
