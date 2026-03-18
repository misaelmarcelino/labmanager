from app.shared.config.standin.logs_config import logger


def remove_duplicates(file_origin, output_path):

    logger.info("Validando e removendo linhas duplicadas")

    try:

        with open(file_origin, "r") as file:
            lines = file.readlines()

        # mantém ordem e remove duplicados
        unique_lines = list(dict.fromkeys(lines))

        with open(output_path, "w") as file:
            for line in unique_lines:
                file.write(line)

        logger.info("Duplicidades removidas com sucesso!")

        return output_path

    except Exception as e:
        logger.error(f"Erro ao remover duplicidades: {e}")
        return None