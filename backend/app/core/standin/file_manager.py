import os
import shutil
from app.shared.config.standin.logs_config import logger


def move_to_data(source_path, data_dir):

    logger.info(f"Movendo arquivo {source_path}")

    try:

        os.makedirs(data_dir, exist_ok=True)

        filename = os.path.basename(source_path)

        destination = os.path.join(data_dir, filename)

        shutil.move(source_path, destination)

        logger.info("Arquivo movido com sucesso")

        return destination

    except Exception as e:

        logger.error(f"Erro ao mover arquivo: {e}")

        return None