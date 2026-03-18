from pathlib import Path
import shutil

from app.shared.config.standin.logs_config import logger


def distribute_package(package_path, destination_dir):

    logger.info("Distribuindo pacote")

    try:

        package_path = Path(package_path)
        destination_dir = Path(destination_dir)

        if not package_path.exists():
            raise FileNotFoundError(f"Pacote não encontrado: {package_path}")

        destination_dir.mkdir(parents=True, exist_ok=True)

        destination = destination_dir / package_path.name

        shutil.copy2(package_path, destination)

        logger.info(f"Pacote distribuído com sucesso: {destination}")

        return destination

    except Exception as e:

        logger.error(f"Erro na distribuição: {e}")
        raise