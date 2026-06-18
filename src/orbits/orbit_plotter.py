"""
Módulo de Visualización Orbital (V2.0.2).

Capa de presentación encargada de generar objetos gráficos interactivos en 3D
utilizando Poliastro y Plotly, con control directo del color de la órbita y del cuerpo central.
"""

from poliastro.plotting import OrbitPlotter3D
from poliastro.twobody import Orbit
from plotly.graph_objs import Figure
from ..core.logger import get_logger
from ..core.exceptions import SpaceToolkitError

logger = get_logger(__name__)


class OrbitVisualizer:
    """
    Clase responsable de la representación visual interactiva de trayectorias orbitales en 3D.
    """

    def __init__(self):
        """
        Inicializa el visualizador de órbitas.
        """
        logger.info("OrbitVisualizer 3D inicializado.")

    def get_3d_figure(
        self,
        orbit: Orbit,
        name: str = "Órbita",
        orbit_color: str = "#e74c3c",
        earth_color: str = "#3498db",
    ) -> Figure:
        """Genera un objeto de figura 3D interactiva con colores personalizados."""
        if not isinstance(orbit, Orbit):
            logger.error("Se intentó graficar un objeto que no es de tipo Orbit.")
            raise SpaceToolkitError(
                "El objeto proporcionado no es una instancia válida."
            )

        logger.info(f"Generando modelo 3D para: {name}")

        try:
            plotter = OrbitPlotter3D()
            plotter.plot(orbit, label=name)

            fig = plotter._figure

            # --- CONTROL DE COLORES INFALIBLE (Por Geometría) ---
            for trace in fig.data:
                # 1. Si es una superficie esférica -> Es la Tierra
                if trace.type == "surface":
                    trace.update(
                        colorscale=[[0, earth_color], [1, earth_color]], showscale=False
                    )
                # 2. Si es una línea o punto en el espacio -> Es la Órbita
                elif trace.type == "scatter3d":
                    trace.update(
                        line=dict(color=orbit_color), marker=dict(color=orbit_color)
                    )
            # ----------------------------------------------------

            # Ajustes estéticos finales
            fig.update_layout(
                title=f"Visor Espacial 3D: {name}",
                title_x=0.5,
                margin=dict(l=0, r=0, t=50, b=0),
                height=600,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            return fig

        except Exception as e:
            logger.error(f"Fallo al generar el modelo 3D: {e}", exc_info=True)
            raise SpaceToolkitError(f"Error en el motor gráfico orbital: {e}")
