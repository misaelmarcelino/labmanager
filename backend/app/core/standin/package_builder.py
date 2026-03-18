import os
import subprocess
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from app.shared.config.standin.logs_config import logger


DATE_NOW = datetime.now().strftime("%d%m%Y")
PATH_7Z = r"C:\Program Files\7-Zip\7z.exe"
DS_PASSWORD = os.getenv("STANDIN_DS_PASSWORD")


TARGETS = {
    "normal": {
        "scripts": ["Atualizador_V4.sh", "Atualizador.bat"],
        "encrypted": False
    },
    "ds": {
        "scripts": ["Atualizador.sh", "Atualizador.bat"],
        "encrypted": True
    }
}


def create_package(db_path, package_origin, apl_name, apl_ds_name, version):

    logger.info("Iniciando criação dos pacotes")

    packages = [
        (apl_name, "normal"),
        (apl_ds_name, "ds")
    ]

    pac_files = []

    for apl, target in packages:

        package_dir = Path(package_origin) / apl / apl

        if package_dir.exists():
            shutil.rmtree(package_dir)

        standin_dir = package_dir / "standin"
        standin_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(db_path, standin_dir)

        create_scripts(package_dir, apl, target)

        pac_path = build_pac(package_origin, apl, version, target)

        pac_files.append(pac_path)

    return pac_files

def create_scripts(package_dir, apl_name, target):

    sh_file = package_dir / "Atualizador_V4.sh"
    sh_file_ds = package_dir / "Atualizador.sh"
    win_file = package_dir / "Atualizador.bat"

    # ---------- SCRIPT NORMAL ----------
    if target == "normal":

        with open(sh_file, "w", encoding='utf-8', newline='\n') as file:

            file.write("#!/bin/sh\n")
            file.write("#Atualizacao\n")
            file.write("data_formatada=$(date +%d_%m_%Y_%H_%M_%S)\n")
            file.write(f"LOG_1='/var/validaabastece/log/{apl_name}.log'\n")
            file.write(f"LOG_2='/home/pi/EDI/atualizacaorealizada_'$data_formatada'.pr'\n")
            file.write("clear\n")
            file.write(f'echo "[`date`] == Atualização {apl_name}" >> $LOG_1\n')
            file.write('echo "Itens Atualizados:" >> $LOG_1\n')
            file.write(f'echo "Standin {DATE_NOW}" >> $LOG_1\n')
            file.write('echo "Iniciando Atualizacao [...]" >> $LOG_1\n')
            file.write('sleep 2\n')
            file.write(f'sudo mv /var/validaabastece/tmp/{apl_name}/standin/* /var/abastece/dados/ >> $LOG_1\n')
            file.write('sudo chmod 777 -f /var/abastece/dados/standin.db\n')
            file.write('echo "Gravando arquivo VERSION" >> $LOG_1\n')
            file.write(f'echo "{DATE_NOW}" > /var/abastece/dados/STANDIN_VERSION\n')
            file.write(f'echo "[`date`] == Finalização Atualização {apl_name}" >> $LOG_1\n')

            file.write(f'echo "{apl_name}.pac" >> $LOG_2\n')
            file.write(f'sudo mv "/home/pi/EDI/atualizacaorealizada_$data_formatada.pr" "/home/pi/EDI/1.ENVIO/RETORNO_DS/"\n')

    # ---------- SCRIPT DS ----------
    if target == "ds":

        with open(sh_file_ds, "w", encoding='utf-8', newline='\n') as file:

            file.write("#!/bin/sh\n")
            file.write("#Atualizacao\n")
            file.write("data_formatada=$(date +%d_%m_%Y_%H_%M_%S)\n")
            file.write(f"LOG_1='/var/DS_SFTP/logs/{apl_name}.log'\n")
            file.write(f"LOG_2='/home/pi/EDI/atualizacaorealizada_'$data_formatada'.pr'\n")
            file.write("clear\n")
            file.write(f'echo "[`date`] == Atualização {apl_name}" >> $LOG_1\n')
            file.write('echo "Itens Atualizados:" >> $LOG_1\n')
            file.write(f'echo "Standin {DATE_NOW}" >> $LOG_1\n')
            file.write('sleep 2\n')
            file.write(f'sudo mv /var/DS_SFTP/temp/{apl_name}/standin/* /var/abastece/dados/ >> $LOG_1\n')
            file.write('sudo chmod 777 -f /var/abastece/dados/standin.db\n')
            file.write(f'echo "{DATE_NOW}" > /var/abastece/dados/STANDIN_VERSION\n')
            file.write(f'echo "[`date`] == Finalização Atualização {apl_name}" >> $LOG_1\n')

            file.write(f'echo "{apl_name}.pac" >> $LOG_2\n')
            file.write(f'sudo mv "/home/pi/EDI/atualizacaorealizada_$data_formatada.pr" "/home/pi/EDI/1.ENVIO/RETORNO_DS/"\n')

    # ---------- SCRIPT WINDOWS (AMBOS) ----------

    with open(win_file, 'w', encoding='utf-8') as file:

        file.write('@echo off\n')
        file.write(f'echo ===== Atualizacao {apl_name} ===== >> C:\\Valida_Abastece\\Log\\{apl_name}\n')
        file.write(f'set standin_version={DATE_NOW}\n')
        file.write(f'set item_1={DATE_NOW}\n')
        file.write('echo %item_1%>C:\\Valida_Abastece\\Log\\standin.log\n')
        file.write(f'echo Iniciando movimentacao do banco standin.db >> C:\\Valida_Abastece\\Log\\{apl_name}.log\n')
        file.write(f'xcopy /E /S /Y /Q C:\\Valida_Abastece\\packs\\{apl_name}\\standin\\standin.db C:\\Abastece\\ServicoAbastece\\Data >> C:\\Valida_Abastece\\Log\\{apl_name}.log\n')
        file.write('echo %standin_version%>C:\\Abastece\\ServicoAbastece\\Data\\STANDIN_VERSION\n')
        file.write(f'echo Termino da execucao >> C:\\Valida_Abastece\\Log\\{apl_name}.log\n')
        file.write('exit\n')
        
def build_pac(package_origin, apl_name, version, target):

    base_package = Path(package_origin) / apl_name / apl_name 
    build_dir = base_package.parent / f"build_{target}"

    if build_dir.exists():
        shutil.rmtree(build_dir)

    shutil.copytree(base_package, build_dir)

    config = TARGETS[target]

    # remove scripts desnecessários
    for file in build_dir.glob("Atualizador*"):
        if file.name not in config["scripts"]:
            file.unlink()

    zip_path = (Path(package_origin) / f"{apl_name}.zip").resolve()

    if config["encrypted"]:

        cmd = [
            PATH_7Z,
            "a",
            "-tzip",
            "-mem=ZipCrypto",
            f"-p{DS_PASSWORD}",
            str(zip_path),
            "."
        ]

        proc = subprocess.run(
            cmd,
            cwd=build_dir,
            capture_output=True,
            text=True
        )

        if proc.returncode != 0:
            raise RuntimeError(f"Erro ao criar pacote DS: {proc.stderr}")

    else:

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_ref:

            for root, _, files in os.walk(build_dir):

                for file in files:

                    path = os.path.join(root, file)

                    arcname = os.path.join(
                        apl_name,
                        os.path.relpath(path, build_dir)
                    )

                    zip_ref.write(path, arcname)

    pac_path = zip_path.with_suffix(".pac")

    shutil.move(zip_path, pac_path)

    logger.info(f"Pacote criado: {pac_path}")

    shutil.rmtree(build_dir)

    return pac_path