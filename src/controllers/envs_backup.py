from repositories.backup import BackupRepository
import shutil, os


class EnvsBackup(BackupRepository):

    def set_up(self):
        self.path_env = "/etc/cisbaf-setup"
    
    def run(self):
        for item in os.listdir(self.path_env):
            s = os.path.join(self.path_env, item)
            d = os.path.join(self.path_backup, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)