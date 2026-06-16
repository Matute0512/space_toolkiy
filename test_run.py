"""
Script temporal para probar el flujo completo del Módulo de Exoplanetas.
"""

from src.exoplanets.data_loader import ExoplanetDataLoader
from src.exoplanets.analyzer import ExoplanetAnalyzer
from src.exoplanets.visualizer import ExoplanetVisualizer
from src.core.exceptions import SpaceToolkitError


def main():
    print("🚀 Iniciando prueba de conexión con la NASA...\n")

    try:
        # --- 1. Capa de Datos ---
        print("📥 Paso 1: Extrayendo datos...")
        loader = ExoplanetDataLoader()
        raw_df = loader.load_data()

        # --- 2. Capa de Lógica de Negocio ---
        print("\n🧠 Paso 2: Analizando y limpiando datos...")
        analyzer = ExoplanetAnalyzer(raw_df)
        analyzer.clean_data()

        # Obtenemos la métricas
        stats = analyzer.get_discovery_methods_stats()
        candidates = analyzer.filter_earth_like_candidates()

        # --- 3. Capa de presentacíon ---
        print("\n📊 Paso 3: Renderizando gráficos...")
        visualizer = ExoplanetVisualizer()

        print(
            "   -> Mostrando gráfico 1 (Cierra la ventana del gráfico para continuar)"
        )
        visualizer.plot_discovery_methods(stats=stats)

        print(
            "   -> Mostrando gráfico 2 (Cierra la ventana del gráfico para continuar)"
        )
        visualizer.plot_mass_vs_radius(candidates_df=candidates)

        print("\n✨ ¡Prueba del módulo de exoplanetas finalizada con éxito!")

    except SpaceToolkitError as e:
        print(f"\n❌ Error en el toolkit: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
