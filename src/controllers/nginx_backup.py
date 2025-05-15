from repositories.backup import BackupRepository
import os
import shutil
import subprocess
import datetime

class NginxBackup(BackupRepository):
    def set_up(self):
        self.path_files_nginx = "/home/cisbaf/servers/nginx-service/files-nginx"
        self.backup_filename = os.path.join(self.path_backup, f"nginx_backup.tar")

    def run(self):
        # Garante permissões (se necessário)
        command = ["sudo", "-S", "chmod", "-R", "777", self.path_files_nginx]
        senha = "7890380\n"
        
        subprocess.run(
            command,
            input=senha.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        # Empacota a pasta em um .tar (sem compressão)
        shutil.make_archive(
            base_name=self.backup_filename.replace('.tar', ''),
            format='tar',  # Apenas empacota, sem compactar
            root_dir=os.path.dirname(self.path_files_nginx),
            base_dir=os.path.basename(self.path_files_nginx))
        
        self.register_log("info", f"Arquivo .tar criado em: {self.backup_filename}")