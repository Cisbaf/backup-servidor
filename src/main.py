from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from controllers.envs_backup import EnvsBackup
from controllers.mysql_backup import MysqlBackup
from controllers.zabbix_backup import ZabbixBackup
from controllers.nginx_backup import NginxBackup
from controllers.git_backup import GitRemoteBackup
from utils.path import find_folder_path
from repositories.backup import BackupRepository, logger
from typing import List, Type
from dirsync import sync

ENV_GLOBAL = "/etc/cisbaf-setup/cisbaf-global-envs.conf"

load_dotenv(ENV_GLOBAL)

backups: List[Type[BackupRepository]] = [
    GitRemoteBackup,
    NginxBackup,
    EnvsBackup, 
    MysqlBackup,
    ZabbixBackup
]

if __name__ == "__main__":

    with ThreadPoolExecutor(max_workers=3) as executor:
        logger.info(f"Inicializando {len(backups)} backups!")
        for backup_class in backups:
            executor.submit(backup_class().start)
    
    sync(find_folder_path("setup/backups"), '/mnt/cisbaf_backup', 'sync', purge=False)
