"""
Módulo de Visualización Orbital.

Capa de presentación encargada de renderizar órbitas físicas
en 2D utilizando el motor gráfico de Poliastro y Matplotlib.
"""

import matplotlib.pyplot as plt
from poliastro.plotting import StaticOrbitPlotter
from poliastro.twobody import Orbit

from ..core.logger import get_logger
from ..core.exceptions import SpaceToolkitError

logger = get_logger(__name__)


class OrbitVisualizer:
    """Clase responsable de la representación visual estática de trayectorias orbitales."""

    def __init__(self):
        """Incializa el visualizador de órbitas."""
        logger.info("OrbitVisualizer inicializado.")

    def plot_2d(self, orbit: Orbit, name: str = "Órbita") -> None:
        """Generar y muestra un dráfico 2D de la órbita especificada vista desde el polo.

        Args:
            orbit (Orbit): Objeto de órbita generado por el motor físico.
            name (str, optional): Nombre del objeto orbital para la etiqueta del gráfico.
                Por defecto "Órbita".

        Returns:
            None

        Raises:
            SpaceToolkitError: Si el objeto de órbita no es válido o ocurre un error al graficar.
        """
        if not isinstance(orbit, Orbit):
            logger.error("Se intentó graficar un objeto que no es de tipo Orbit.")
            raise SpaceToolkitError(
                "El objeto proporcionado no es una instancia de Orbit válida."
            )

        logger.info(f"Generando visualización 2D para: {name}")

        try:
            # Creamos la figura explícitamente para controlar el tamaño
            fig, ax = plt.subplots(figsize=(8, 8))
            plotter = StaticOrbitPlotter(ax)

            # Poliastro dibuja automáticamente la Tierra en el centro y añade la órbita
            plotter.plot(orbit, label=name)

            # Ajustes estéticos finales
            plt.title(f"Visualización Orbital 2D: {name}", fontsize=14, weight="bold")
            plt.tight_layout()

            # Mostramos la ventana interactiva
            plt.show()

        except Exception as e:
            logger.error(f"Fallo al renderizar la órbita: {e}")
            raise SpaceToolkitError(f"Error en la capa de presentación orbital: {e}")
