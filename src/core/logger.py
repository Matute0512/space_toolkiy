"""
Módulo de Observabilidad.

Proporciona la configuración estándar de registro (logging) para el Toolkit Espacial.
Separa los mensajes informativos en consola de los registros de error persistentes.
"""

import logging
import sys
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """Crea y configura una instancia de logger para el módulo solicitante.

    Args:
        name (str): El nombre del módulo que invoca logger (generalmente __name__).

    Returns:
        logging.Logger: Instancia configurada lista para registrar eventos.
    """
    logger = logging.getLogger(name)

    # Evita duplicar handlers si la función se llama multiples veces
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Definir un formato estándar: Fecha | Nivel | Origen | Mensaje
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler 1: Consola (Solo INFO o superior)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler 2: Archivo (Solo WARNING o superior para mantenimiento)
        # SUBE 3 niveles desde este archivo para colocar el log en la raíz del repositorio
        base_dir = Path(__file__).resolve().parent.parent.parent
        log_file = base_dir/"space_toolkit.log"

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
