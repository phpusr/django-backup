def backup_db():
    backup_service = BackupService()
    backup_service.backup_db()
    backup_service.delete_old_files(30)

class BackupService:
    def backup_db(self):
        pass

    def delete_old_files(self, days: int):
        pass
