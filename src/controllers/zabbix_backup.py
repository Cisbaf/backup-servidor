from repositories.backup import BackupRepository
import shutil
import os


class ZabbixBackup(BackupRepository):
    
    def set_up(self):
        self.path_docker_compose = "/home/cisbaf/servers/zabbix/docker-compose.yml"
        self.grafana_volume = "zabbix_grafana-data"
        self.zabbix_volume = "zabbix_zabbix-server-data"
        self.granafa_container_name = "grafana"
        self.zabbix_container_name = "zabbix-server"

    def run(self):
        # Copiar docker compose
        shutil.copy2(self.path_docker_compose, self.path_backup)
        volume_grafana = self.docker.volumes.get(self.grafana_volume)
        volume_zabbix = self.docker.volumes.get(self.zabbix_volume)

        grafana_container = self.docker.containers.get(self.granafa_container_name)
        zabbix_container = self.docker.containers.get(self.zabbix_container_name)

        # Salvar volume do grafana
        with open(os.path.join(self.path_backup, "grafana_volume.tar"), "wb") as f:
            exit_code, (stdout, stderr) = grafana_container.exec_run(
                ["tar", "cf", "-", "-C", "/var/lib/grafana", "."],
                demux=True
            )

            if exit_code != 0:
                error_msg = stderr.decode() if stderr else "Sem mensagem de erro."
                return self.register_log("critical", f"Erro ao criar o backup do volume (exit code {exit_code}): {error_msg}")
        
            f.write(stdout)
            self.register_log("info", "Volume do grafana salvo!")

        # Salvar volume do zabbix
        with open(os.path.join(self.path_backup, "zabbix_volume.tar"), "wb") as f:
            exit_code, (stdout, stderr) = zabbix_container.exec_run(
                ["tar", "cf", "-", "-C", "/var/lib/zabbix", "."],
                demux=True
            )

            if exit_code != 0:
                error_msg = stderr.decode() if stderr else "Sem mensagem de erro."
                return self.register_log("critical", f"Erro ao criar o backup do volume (exit code {exit_code}): {error_msg}")
            
            f.write(stdout)
            self.register_log("info", "Volume do zabbix salvo!")