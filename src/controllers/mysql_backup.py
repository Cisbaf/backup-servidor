from repositories.backup import BackupRepository
import os
import shutil

class MysqlBackup(BackupRepository):

    def set_up(self):
        self.container_name = "mysql-container"
        self.mysql_user = "root"
        self.mysql_pass = os.getenv("MYSQL_PASS")
        self.configs_mysql_path = "/home/cisbaf/databases"

    def run(self):
        # Verifica se o container existe
        container = self.docker.containers.get(self.container_name)
        if not container:
            return self.register_log("error", f"Container {self.container_name} não encontrado!")
        # Comando para gerar o dump (sem senha na linha de comando)
        dump_command = ["mysqldump", "-u", self.mysql_user, "--all-databases"]
        # Executa o comando dentro do container
        exit_code, (stdout, stderr) = container.exec_run(
            dump_command,
            demux=True,
            environment={'MYSQL_PWD': self.mysql_pass},
        )
        # Verifica a saída
        if exit_code != 0:
            error_msg = stderr.decode() if stderr else "Sem mensagem de erro."
            return self.register_log("error", f"Erro ao executar mysqldump (exit code {exit_code}): {error_msg}")
        # Se stdout estiver vazio, pode indicar um problema
        if not stdout:
            return self.register_log("error", "O dump foi gerado, mas não retornou dados.")
        # Escrevendo o conteúdo em arquivo
        with open(f"{self.path_backup}/data.sql", "wb") as file:
            file.write(stdout)
        # Copiando arquivos de configuração do mysql
        if os.path.exists(self.configs_mysql_path):
            for file in os.listdir(self.configs_mysql_path):
                path_file = os.path.join(self.configs_mysql_path, file)
                path_dest = os.path.join(self.path_backup, file)
                shutil.copy2(path_file, path_dest)
        # Finalizando
        self.register_log("info", f"Dados salvo com sucesso em {self.path_backup}")
