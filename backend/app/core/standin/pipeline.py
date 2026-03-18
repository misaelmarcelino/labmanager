from pathlib import Path
from datetime import datetime
from app.shared.config.standin.logs_config import logger
from app.core.standin.parser import remove_duplicates
from app.core.standin.database_builder import create_database
from app.core.standin.package_builder import create_package
from app.core.standin.distributor import distribute_package
from app.core.standin.cleanup import clean_work_dirs
from app.core.standin.job_manager import update_job, finish_job

VERSION = datetime.now().strftime("%d%m%Y")
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
PACKAGE_DIR = Path("packages")

APL_NAME = f"APL_STANDIN_{VERSION}"
APL_DS_NAME = f"APL_DS_STANDIN_{VERSION}"
# NETWORK_DISTRIBUTION = Path(r"\\bredt1-svfsvp02\\AXWAY_BACKUP\\EDI\\1.ENVIO\\6.SFTP_CREDENCIADOS\\Envio_geral_ABAST")

def run_pipeline(file_path, job_id):

    logger.info("=== INICIANDO PIPELINE STANDIN ===")

    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    PACKAGE_DIR.mkdir(exist_ok=True)

    # 1 remover duplicidades
    processed_file = DATA_DIR / "standin.txt"
    
    update_job(job_id, "Processando TXT")
    logger.info("Processando TXT")
    remove_duplicates(file_path, processed_file)

    # 2 criar banco
    db_path = OUTPUT_DIR / "standin.db"

    update_job(job_id, "Criando banco de Dados")
    logger.info("Criando banco SQLite")
    create_database(processed_file, db_path, job_id)

    # 3 criar pacotes
    update_job(job_id, "Criando pacotes")
    logger.info("Criando pacotes PAC")

    pac_paths = create_package(
        db_path,
        PACKAGE_DIR,
        APL_NAME,
        APL_DS_NAME,
        VERSION
    )

    # 4 distribuir
    DISTRIBUTION_DIR = Path("distribution")

    DESTINATIONS = [
        DISTRIBUTION_DIR,
        # NETWORK_DISTRIBUTION
    ]
    
    destinations = []

    for pac in pac_paths:
        update_job(job_id, "Enviando pacote")
        logger.info(f"Distribuindo pacote {pac}")

        for dest in DESTINATIONS:

            destination = distribute_package(
                pac,
                dest
            )

            destinations.append(destination)


    # 5 limpar diretórios de trabalho
    update_job(job_id, "Limpando diretórios temporários")
    logger.info("Limpando diretórios temporários")

    clean_work_dirs(
        DATA_DIR,
        OUTPUT_DIR,
        PACKAGE_DIR,
    )

    finish_job(job_id, 'Processo de envio finalizado!')
    logger.info("=== PIPELINE FINALIZADO ===")

    return destinations