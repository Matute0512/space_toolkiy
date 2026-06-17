"""
Módulo de Visualización de Exoplanetas.

Capa de presentación encargada de generar gráficos y representaciones visuales
a partir de datos procesados, utilizando Matplotlib.
"""

import matplotlib.pyplot as plt
import pandas as pd
from ..core.logger import get_logger
from ..core.exceptions import SpaceToolkitError

# Inicializamos el logger
logger = get_logger(__name__)


class ExoplanetVisualizer:
    """Clase responsable de la renderización de gráficos para el análisis de exoplanetas."""

    def __init__(self):
        """Inicializa el visualizador y configura el estilo base de Matplotlib."""
        # Usamos el estilo predeterminado limpio para gráficos científicos.
        plt.style.use("seaborn-v0_8-darkgrid")
        logger.info("Visualizer inicializado con estilo de gráficos configurado.")

    def plot_discovery_methods(self, stats: pd.Series) -> None:
        """Genera y muestra un gráfico de barras con las estadísticas de métodos de descubrimiento.

        Args:
            stats (pd.Series): Serie de Pandas con el conteo de métodos (proveída por el Analyzer).
        """
        if stats is None or stats.empty:
            logger.error("No se pueden graficar estadísticas vacías.")
            raise SpaceToolkitError("Datos estadísticos insuficientes para graficar.")

        logger.info("Generando gráfico de métodos de descubrimiento...")

        plt.figure(figsize=(10, 6))
        # Seleccionamos los 5 métodos más exitosos
        top_stats = stats.head(5)

        bars = plt.bar(
            top_stats.index, top_stats.to_numpy(), color="#1f77b4", edgecolor="black"
        )

        plt.title(
            "Top 5 Métodos de Descubrimiento de Exoplanetas", fontsize=14, weight="bold"
        )
        plt.xlabel("Método de Descubrimineto", fontsize=12)
        plt.ylabel("Cantidad de Planetas Confirmados", fontsize=12)
        plt.xticks(rotation=15)

        # Añadir el número exacto encima de cada barra
        for bar in bars:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 50,
                f"{int(yval)}",
                ha="center",
                va="bottom",
            )

        plt.tight_layout()
        plt.show()

    def plot_mass_vs_radius(self, candidates_df: pd.DataFrame) -> None:
        """Genera un gráfico de dispersión relacionando la masa y el radio de candidatos tipo Tierra.

        Args:
            candidates_df (pd.DataFrame): DataFrame filtrado con los candidatos.
        """
        if candidates_df is None or candidates_df.empty:
            logger.warning("No hay candidatos tipo Tierra para graficar.")
            return

        logger.info("Generando gráfico de dispersión de Masa vs Radio...")

        plt.figure(figsize=(8, 8))
        plt.scatter(
            candidates_df["pl_bmasse"],
            candidates_df["pl_rade"],
            alpha=0.7,
            c="#d62728",
            edgecolors="k",
            s=50,
        )

        plt.title("Candidatos tipo Tierra: Masa vs Radio", fontsize=14, weight="bold")
        plt.xlabel("Masa (Masas Terrestres)", fontsize=12)
        plt.ylabel("Radio (Radios Terrestres)", fontsize=12)

        # Agregamos líneas de referencia en 1.0 (los valores exactos de la Tierra)
        plt.axvline(
            x=1.0, color="blue", linestyle="--", alpha=0.5, label="Masa de la Tierra"
        )
        plt.axhline(
            y=1.0, color="green", linestyle="--", alpha=0.5, label="Radio de la Tierra"
        )

        plt.legend()
        plt.tight_layout()
        plt.show()
