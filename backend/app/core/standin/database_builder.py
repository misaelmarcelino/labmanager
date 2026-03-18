import sqlite3
from pathlib import Path
from app.shared.config.standin.logs_config import logger
from app.core.standin.job_manager import update_job

def create_database(file_txt, db_path, job_id):

    logger.info("Iniciando criação do banco standin")

    try:

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS standin (
                DS_TAG TEXT PRIMARY KEY NOT NULL,
                DS_PLACA TEXT NOT NULL
            )
        """)

        cursor.execute("INSERT INTO standin (DS_TAG, DS_PLACA) VALUES ('0000DS_TAG', 'DS_PLACA');")

        with open(file_txt) as file:

            for line in file:

                tag, placa = line.strip().split(";")

                cursor.execute(
                    "INSERT OR IGNORE INTO standin (DS_TAG, DS_PLACA) VALUES (?, ?)",
                    (tag, placa)
                )

        cursor.execute("SELECT COUNT(*) FROM standin")
        total = cursor.fetchone()[0]

        update_job(jod_id, f"Total de registros no banco: {total}")
        logger.info(f"Total de registros no banco: {total}")

        conn.commit()
        cursor.execute("VACUUM")
        conn.close()

        return db_path

    except Exception as e:

        logger.error(f"Erro ao criar banco: {e}")

        return None