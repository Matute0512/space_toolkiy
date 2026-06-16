"""
Módulo de Análisis de Exoplanetas.

Capa de lógica de negocio responsable de limpiar,transformar y analizar
matemáticamente los datos extraidos de la NASA utilizando Pandas.
"""

import pandas as pd
from ..core.logger import get_logger
from ..core.exceptions import DataValidationError

# Inicializamos el logger para el analizador
logger = get_logger(__name__)


class ExoplanetAnalyzer:
    """Clase para procesar, limpiar y analizar datos de exoplanetas."""

    def __init__(self, df: pd.DataFrame):
        """Inicializa el analizador con un DataFrame crudo.

        Args:
            df (pd.DataFrame): Datos extraídos directamente de la capa de datos.
        """
        if df is None or df.empty:
            raise DataValidationError(
                "El DataFrame proporcionado al Analyzer está vacío o es nulo.")

        # Trabajamos con una copia para aplicar el principio de inmutabilidad
        # y no alterar los datos crudos originales en memoria.
        self.df = df.copy()
        logger.info(
            f"Analyzer inicializado correctamente con {len(self.df)} registros")

    def clean_data(self) -> pd.DataFrame:
        """Limpia el DataFrame normalizando formatos y menejando valores nulos.

        Returns:
            pd.DataFrame: El DataFrame limpio listo para análisis o visualizacion.
        """
        logger.info("Iniciando proceso de limpieza de datos...")

        # 1. Normalizar el año de descubrimiento (de float a int), llenando nulos con 0
        self.df['disc_year'] = self.df['disc_year'].fillna(0).astype(int)

        # 2. Registrar la cantidad de datos faltantes en métricas fisicas críticas.
        missing_mass = self.df['pl_bmasse'].isna().sum()
        missing_radius = self.df['pl_rade'].isna().sum()

        logger.info(
            f"Reporte de completitud: Faltan datos de masa en {missing_mass} planetas y de radio en {missing_radius}.")

        return self.df

    def get_discovery_methods_stats(self) -> pd.Series:
        """Calcula la cantidad de planetas descubiertos por cada método (ej. Tránsito, Velocidad Radial).

        Returns:
            pd.Series: Serie de Pandas con el conteo ordenado de métodos.
        """
        stats = self.df['discoverymethod'].value_counts()
        logger.info("Estadísticas de métodos de descubrimineto calculadas.")
        return stats

    def filter_earth_like_candidates(self) -> pd.DataFrame:
        """Filtra planetas con características físicas vagamente similares a la Tierra.
        Criterios arbitrarios: Radio entre 0.8 y 1.5 radios terrestres,
        y Masa entre 0.5 y 5.0 masas terrestres.

        Returns:
            pd.DataFrame: DataFrame filtrado solo con los candidatos.
        """
        logger.info("Buscando candidatos simulares a la Tierra (Earth-like)...")

        # Columnas: pl_rade (Radio en radios terrestres), pl_bmasse (Masa en masas terrestres)
        condition = ((self.df['pl_rade'] >= 0.8) & (self.df['pl_rade'] <= 1.5) &
                     (self.df['pl_bmasse'] >= 0.5) & (
                         self.df['pl_bmasse'] <= 5.0)
                     )

        candidates = self.df[condition]
        logger.info(
            f"Se encontraron {len(candidates)} candidatos potenciales.")

        return candidates
