"""
Punto de entrada para la Interfaz Web (Dashboard) del Space Toolkit.
Construido con Streamlit para la versión 2.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Capa de Exoplanetas
from src.exoplanets.data_loader import ExoplanetDataLoader
from src.exoplanets.analyzer import ExoplanetAnalyzer

# Capa de Órbitas (Agrega estas líneas)
from src.orbits.tle_parser import TLEParser
from src.orbits.physics_engine import PhysicsEngine
from src.orbits.orbit_plotter import OrbitVisualizer

# 1. Configuración principal de la página
st.set_page_config(page_title="Space Toolkit", page_icon="🚀", layout="wide")

# 2. Sistema de Caché en RAM


@st.cache_data
def load_and_clean_exoplanet_data() -> pd.DataFrame:
    """Extrae, carga y limpia los datos de exoplanetas.

    Returns:
        pd.DataFrame: DataFrame con los datos de exoplanetas limpios.

    Raises:
        Exception: Si ocurre un error en la carga o limpieza de datos.
    """
    loader = ExoplanetDataLoader()
    raw_df = loader.load_data()

    analyzer = ExoplanetAnalyzer(raw_df)
    clean_df = analyzer.clean_data()

    return clean_df


# 3. Controladores de Vistas


def render_exoplanets_view():
    """
    Renderiza la vista del módulo de Exoplanetas.

    Returns:
        None
    """
    st.header("🪐 Explorador de Planetas Extrasolares")
    st.markdown("Analiza la base de datos oficial de la NASA en tiempo real.")

    with st.spinner("Cargando y procesando base de datos astrofísica..."):
        try:
            # Cargamos datos base
            df = load_and_clean_exoplanet_data()

            # Instanciamos el analizador nuevamente para calcular el ESI
            analyzer = ExoplanetAnalyzer(df)
            esi_df = analyzer.calculate_esi()

            # --- SECCIÓN: CONTROLES INTERACTIVOS ---
            st.subheader("Filtros Físicos")
            col1, col2 = st.columns(2)

            with col1:
                min_esi = st.slider(
                    "Puntaje mínimo de Similitud Terrestre (ESI)",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.8,
                    step=0.05,
                )
            with col2:
                max_distance = st.number_input(
                    "Distancia máxima a la Tierra (Años Luz)", value=5000
                )

            # Aplicamos los filtros del usuario
            filtered_df = esi_df[esi_df["esi_score"] >= min_esi]

            st.success(
                f"Se encontraron **{len(filtered_df)}** exoplanetas que cumplen con los criterios."
            )

            # --- SECCIÓN: GRÁFICO INTERACTIVO PLOTLY ---
            st.subheader("Candidatos Prometedores: Masa vs Radio")

            if not filtered_df.empty:
                # Gráfico de dispersión interactivo
                fig = px.scatter(
                    filtered_df,
                    x="pl_bmasse",
                    y="pl_rade",
                    color="esi_score",  # El color cambia según el ESI
                    hover_name="pl_name",
                    hover_data=["disc_year", "discoverymethod", "esi_score"],
                    color_continuous_scale="Viridis",
                    labels={
                        "pl_bmasse": "Masa (Masas Terrestres)",
                        "pl_rade": "Radio (Radios Terrestres)",
                        "esi_score": "Puntaje ESI",
                    },
                )

                # Líneas de referencia de la Tierra
                fig.add_hline(
                    y=1.0,
                    line_dash="dash",
                    line_color="green",
                    annotation_text="Radio Tierra",
                )
                fig.add_vline(
                    x=1.0,
                    line_dash="dash",
                    line_color="blue",
                    annotation_text="Masa Tierra",
                )

                # Renderizamos en Streamlit
                st.plotly_chart(fig, use_container_width=True)

                # Mostramos la tabla de los mejores candidatos
                st.write("Top Candidatos (Datos Tabulares):")
                st.dataframe(
                    filtered_df[
                        [
                            "pl_name",
                            "hostname",
                            "esi_score",
                            "pl_bmasse",
                            "pl_rade",
                            "discoverymethod",
                        ]
                    ].head(10),
                    use_container_width=True,
                )
            else:
                st.warning(
                    "No hay planetas que cumplan con estos filtros tan estrictos."
                )

        except Exception as e:
            st.error(f"Fallo crítico en los sistemas: {e}")


def render_orbits_view():
    """Renderiza la vista del módulo de Astrodinámica con visualización 3D."""
    st.header("🛰️ Simulador de Astrodinámica 3D")
    st.markdown(
        "Calcula y visualiza órbitas terrestres a partir de datos TLE (Two-Line Element)."
    )

    # --- SECCIÓN: ENTRADA DE DATOS TLE ---
    st.subheader("Entrada de Datos Orbitales")

    # TLE por defecto (ISS - Estación Espacial Internacional)
    default_tle = (
        "ISS (ZARYA)\n"
        "1 25544U 98067A   23272.53177699  .00015569  00000-0  28172-3 0  9994\n"
        "2 25544  51.6415 141.0505 0005703  26.0441 334.0838 15.49479361418197"
    )

    tle_input = st.text_area(
        "Pega aquí el conjunto TLE del satélite:",
        value=default_tle,
        height=150,
        help="El TLE debe tener el nombre del objeto y sus dos líneas de datos estándar de 69 caracteres.",
    )

    # Selectores de color interactivos
    orbit_color = st.color_picker("Color de la órbita", "#e74c3c")
    earth_color = st.color_picker("Color de la Tierra", "#3498db")

    if st.button("🚀 Calcular y Renderizar Órbita"):
        try:
            # 1. Capa de Datos: Parseo y Validación
            parser = TLEParser()
            tle_data = parser.parse_tle(tle_input)

            # 2. Capa de Lógica: Motor Físico
            engine = PhysicsEngine()
            with st.spinner(
                "Resolviendo Ecuación de Kepler y propagando trayectoria..."
            ):
                orbit = engine.create_orbit_from_tle(tle_data)

            # 3. Capa de Presentación: Generación del Modelo 3D
            visualizer = OrbitVisualizer()
            fig = visualizer.get_3d_figure(
                orbit,
                name=tle_data["name"],
                orbit_color=orbit_color,
                earth_color=earth_color,
            )

            # Renderizado en la Web
            st.plotly_chart(fig, use_container_width=True)

            # Datos técnicos adicionales
            st.info(
                f"📍 **Objeto:** {tle_data['name']} | **Semieje Mayor:** {orbit.a.to('km'):.2f}"
            )

        except Exception as e:
            st.error(f"Error en el cálculo astrodinámico: {e}")


# 4. Flujo Principal de la Aplicación
def main():
    """
    Punto de entrada principal del Dashboard.

    Returns:
        None
    """
    st.title("🌌 Space Toolkit Dashboard")
    st.divider()

    # Menú lateral de navegación
    st.sidebar.image(
        "https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg", width=100
    )
    st.sidebar.title("Panel de Control")
    st.sidebar.markdown("---")

    modulo_seleccionado = st.sidebar.radio(
        "Selecciona un Sistema Operativo:",
        ["Ciencia de Datos (Exoplanetas)", "Física Orbital (Astrodinámica)"],
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Space Toolkit v2.0-dev | Desarrollado con Python")

    # Enrutamiento dinámico
    if modulo_seleccionado == "Ciencia de Datos (Exoplanetas)":
        render_exoplanets_view()
    elif modulo_seleccionado == "Física Orbital (Astrodinámica)":
        render_orbits_view()


if __name__ == "__main__":
    main()
