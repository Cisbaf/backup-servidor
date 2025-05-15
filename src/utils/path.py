from pathlib import Path

def find_folder_path(folder_name: str) -> Path:
    """
    Procura uma pasta com o nome especificado subindo os diretórios
    a partir do caminho do arquivo atual (__file__).

    :param folder_name: Nome da pasta a ser localizada
    :return: Caminho absoluto para a pasta encontrada
    :raises FileNotFoundError: se a pasta não for encontrada
    """
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        possible_path = parent / folder_name
        if possible_path.is_dir():
            return possible_path

    raise FileNotFoundError(f"Pasta '{folder_name}' não encontrada na hierarquia de diretórios.")

def get_src_path() -> Path:
    """
    Retorna o caminho absoluto da pasta 'src'.
    """
    return find_folder_path("src")
