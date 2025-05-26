from repositories.backup import BackupRepository
import os
import subprocess
import re

class GitRemoteBackup(BackupRepository):

    def set_up(self):
        self.path_servers = "/home/cisbaf/servers"
    
    def run(self):
        folders = [name for name in os.listdir(self.path_servers) if os.path.isdir(os.path.join(self.path_servers, name))]
        links = []
        with open(os.path.join(self.path_backup, 'links.txt'), "w") as file:
            for folder in folders:
                path = os.path.join(self.path_servers, folder)
                try:
                    output = subprocess.check_output(
                        ['git', '-C', path, 'remote', '-v'],
                        stderr=subprocess.STDOUT,  # Captura também erros
                        text=True  # Faz output ser str em vez de bytes
                    )
                    match = re.search(r'(https?://\S+)', output)
                    link = match.group(1)
                    file.write(link + '\n')
                    links.append(link)
                except subprocess.CalledProcessError as e:
                    self.register_log("warning", f"Erro ao executar git remote: {e.output.strip()}, projeto: {folder}")

        self.register_log("info", f"O backup dos links foram concluidos!")
