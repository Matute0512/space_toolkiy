"""
Script maestro para probar el flujo completo del Space Toolkit (v1.0.0).
Incluye el análisis de exoplanetas y la simulación de astrodinámica.
"""

from src.exoplanets.data_loader import ExoplanetDataLoader
from src.exoplanets.analyzer import ExoplanetAnalyzer
from src.exoplanets.visualizer import ExoplanetVisualizer

from src.orbits.tle_parser import TLEParser
from src.orbits.physics_engine import PhysicsEngine
from src.orbits.orbit_plotter import OrbitVisualizer

from src.core.exceptions import SpaceToolkitError


def main():
    print("🚀 Iniciando prueba maestra del Space Toolkit v1.0.0...\n")

    try:
        # =================================================================
        # MÓDULO 1: EXOPLANETAS (CIENCIA DE DATOS)
        # =================================================================
        print("🌌 --- INICIANDO MÓDULO DE EXOPLANETAS ---")
        print("📥 Extrayendo y limpiando datos...")

        exo_loader = ExoplanetDataLoader()
        raw_df = exo_loader.load_data()

        exo_analyzer = ExoplanetAnalyzer(raw_df)
        exo_analyzer.clean_data()
        stats = exo_analyzer.get_discovery_methods_stats()
        candidates = exo_analyzer.filter_earth_like_candidates()

        print("📊 Renderizando gráficos de exoplanetas...")
        exo_visualizer = ExoplanetVisualizer()

        print(
            "   -> (1/3) Gráfico de métodos de descubrimiento (Cierra la ventana para continuar)"
        )
        exo_visualizer.plot_discovery_methods(stats)

        print(
            "   -> (2/3) Gráfico de candidatos Tipo Tierra (Cierra la ventana para continuar)"
        )
        exo_visualizer.plot_mass_vs_radius(candidates)

        # =================================================================
        # MÓDULO 2: ÓRBITAS (SIMULACIÓN FÍSICA)
        # =================================================================
        print("\n🛰️ --- INICIANDO MÓDULO DE ASTRODINÁMICA ---")

        # Datos TLE reales de la Estación Espacial Internacional (ISS)
        iss_tle = """ISS (ZARYA)
                    1 25544U 98067A   23272.53177699  .00015569  00000-0  28172-3 0  9994
                    2 25544  51.6415 141.0505 0005703  26.0441 334.0838 15.49479361418197"""

        print("📥 Parseando TLE y propagando órbita...")
        orbit_parser = TLEParser()
        tle_data = orbit_parser.parse_tle(iss_tle)

        orbit_engine = PhysicsEngine()
        orbit = orbit_engine.create_orbit_from_tle(tle_data)

        print("📊 Renderizando simulación espacial...")
        orbit_visualizer = OrbitVisualizer()

        print(
            f"   -> (3/3) Mostrando órbita de: {tle_data['name']} (Cierra la ventana para terminar)"
        )
        orbit_visualizer.plot_2d(orbit, name=tle_data["name"])

        print(
            "\n✨ ¡Prueba maestra finalizada con éxito! Todos los sistemas operativos."
        )

    except SpaceToolkitError as e:
        print(f"\n❌ Error controlado en el toolkit: {e}")
    except Exception as e:
        print(f"\n❌ Error crítico inesperado: {e}")


if __name__ == "__main__":
    main()
