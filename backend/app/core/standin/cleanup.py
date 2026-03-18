import shutil
from pathlib import Path

from app.shared.config.standin.logs_config import logger


def clean_work_dirs(*dirs):

    for directory in dirs:

        path = Path(directory)

        if not path.exists():
            continue

        for item in path.iterdir():

            try:

                if item.is_file() or item.is_symlink():
                    item.unlink()

                elif item.is_dir():
                    shutil.rmtree(item)

            except Exception as e:
                logger.error(f"Erro ao limpar {item}: {e}")

        logger.info(f"Diretório limpo: {path}")