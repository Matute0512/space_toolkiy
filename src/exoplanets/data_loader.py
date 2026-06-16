"""
Módulo de Carga de Datos de Exoplanetas.

Se encarga de la extracción de datos desde el servicio TAP de la NASA
y de su carga inicial en estructuras de datos de Pandas.
"""

import urllib.parse
import urllib.request
from urllib.error import URLError, HTTPError
import pandas as pd

# Importaciones relativas de nuestra capa core
from ..core.config import NASA_EXOPLANET_TAP_URL, EXOPLANET_CACHE_FILE, NETWORK_TIMEOUT
from ..core.logger import get_logger
from ..core.exceptions import DataDownloadError, DataValidationError, SpaceToolkitError

# Inicializamos el logger para este archivo
logger = get_logger(__name__)


class ExoplanetDataLoader:
    """Clase resonsable de gestionar la descarga y lectura de datos de exoplanetas."""

    def __init__(self):
        # ADQL (Astronomical Data Query Language) para traer solo la data confirmada útil.
        # Traemos: Nombre del planeta, estrella, método de descubrimiento, año, periodo orbital, radio y masa
        self.query = (
            "SELECT pl_name, hostname, discoverymethod, disc_year, "
            "pl_orbper, pl_rade, pl_bmasse "
            "FROM ps WHERE default_flag=1"
        )

    def download_nasa_data(self) -> None:
        """
        Descarga los datos de la NASA usando la API TAP y los guarda localmente.
        Si el archivo ya existe en caché, omite la descarga.
        """
        if EXOPLANET_CACHE_FILE.exists():
            logger.info(
                f"Caché encontrado en {EXOPLANET_CACHE_FILE}. Omitiendo descarga de la NASA."
            )
            return

        logger.info(
            "Iniciando descarga desde el Archivo de Exoplanetas de la NASA. Esto puede tardar unos segundos..."
        )

        params = {"query": self.query, "format": "csv"}

        query_string = urllib.parse.urlencode(params)
        url = f"{NASA_EXOPLANET_TAP_URL}?{query_string}"

        try:
            # Usamos urlretrieve para guardar directamente en nuestro archivo temporal
            urllib.request.urlretrieve(url, EXOPLANET_CACHE_FILE)
            logger.info("Descarga completada y guardada en caché exitosamente.")

        except HTTPError as e:
            logger.error(f"Error del servidor de la NASA: {e.code}")
            raise DataDownloadError(f"La API de la NASA rechazó la conexión: {e}")
        except URLError as e:
            logger.error(f"Fallo de conexión. ¿Hay internet? Detalles: {e.reason}")
            raise DataDownloadError("No se pudo conectar a los servidores de la NASA.")

    def load_data(self) -> pd.DataFrame:
        """
        Carga el archivo CSV local en un DataFrame de Pandas.

        Returns:
            pd.DataFrame: DataFrame crudo con los datos de los exoplanetas.
        """
        # Asegurarnos de que el dato este descargado antes de leerlo
        self.download_nasa_data()

        logger.info("Cargando datos en Pandas DataFrame...")
        try:
            df = pd.read_csv(EXOPLANET_CACHE_FILE)

            if df.empty:
                raise DataValidationError("El archivo CSV descargado está vacio.")

            logger.info(
                f"Datos cargados con éxito: {df.shape[0]} planetas encontrados."
            )
            return df

        except pd.errors.EmptyDataError:
            raise DataValidationError("El archivo CSV está corrupto o vacío.")
        except Exception as e:
            logger.error("Error inesperado al leer el archivo con Pandas.")
            raise SpaceToolkitError(f"Fallo crítico al cargar datos: {e}")
