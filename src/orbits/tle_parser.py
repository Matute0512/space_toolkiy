"""
Módulo de Análisis de Datos TLE.

Capa de datos para la simulación fisica. Se encarga de recibir, validar
y estructurar los datos orbitalse en formato estándar TLE (Two-Line Element).
"""

from ..core.logger import get_logger
from ..core.exceptions import TLEParseError

# Inicializamos el logger
logger = get_logger(__name__)


class TLEParser:
    """Clase responsabale de parsear y validar conjuntos de datos TLE."""

    @staticmethod
    def parse_tle(tle_string: str) -> dict[str, str]:
        """Recibe un String con formato TLE (2 o 3 lineas), lo limpia y valida su estructura.

        Args:
            tle_string (str): Texto crudo con el TLE.

        Returns:
            dict[str,str]: Diccionario con el nombre del satélite y sus dos líneas validas.

        Raises:
            TLEParseError: Si el formato del texto no cumple con el estándar internacional.
        """
        logger.info("Inciando validación y parseo de datos TLE...")

        # Dividimos el texto en líneas, ignorando líneas vacías.
        lines = [
            line.strip() for line in tle_string.strip().split("\n") if line.strip()
        ]

        # Un TLE válido puede tener 2 líneas (sin nombre) o 3 líneas (con nombre).
        if len(lines) == 2:
            name = "Satélite Desconocido"
            line1, line2 = lines
        elif len(lines) == 3:
            name, line1, line2 = lines
        else:
            raise TLEParseError(
                f"El TLE debe tener exactamente 2 o 3 líneas. Se recibieron {len(lines)}."
            )

        # Validación estricta del estándar TLE: cada línea de datos debe tener 69 caracteres
        if len(line1) != 69 or len(line2) != 69:
            raise TLEParseError(
                f"Longitud inválida. Las líneas 1 y 2 deben tener 69 caracteres. "
                f"Línea 1 tiene {len(line1)}, Línea 2 tiene {len(line2)}."
            )

        # Validación de los identificadores de línea
        if not line1.startswith("1 ") or not line2.startswith("2 "):
            raise TLEParseError(
                "Las líneas del TLE no comienzan con los identificadores estándar ('1 ' y '2 ' )."
            )

        logger.info(f"TLE parseado y validado correctamente para el objeto: {name}")

        return {"name": name, "line1": line1, "line2": line2}
