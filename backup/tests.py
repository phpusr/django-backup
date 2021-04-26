from django.test import TestCase

from backup import backup_service


class BackupTests(TestCase):

    def test_backup_is_ok(self):
        res = backup_service.backup_db()
        self.assertIsNotNone(res['id'])
