"""
Script temporal para probar el Módulo de Simulación Física (Órbitas).
"""

from src.orbits.tle_parser import TLEParser
from src.orbits.physics_engine import PhysicsEngine
from src.orbits.orbit_plotter import OrbitVisualizer
from src.core.exceptions import SpaceToolkitError


def main():
    print("🚀 Iniciando prueba del motor astrodinámico...\n")

    # Datos TLE reales de la Estación Espacial Internacional (ISS)
    iss_tle = """ISS (ZARYA)
1 25544U 98067A   23272.53177699  .00015569  00000-0  28172-3 0  9994
2 25544  51.6415 141.0505 0005703  26.0441 334.0838 15.49479361418197"""

    try:
        # --- 1. Capa de Datos ---
        print("📥 Paso 1: Parseando formato TLE...")
        parser = TLEParser()
        tle_data = parser.parse_tle(iss_tle)

        # --- 2. Capa de Lógica de Negocio ---
        print("\n🧠 Paso 2: Calculando parámetros keplerianos y propagando órbita...")
        engine = PhysicsEngine()
        orbit = engine.create_orbit_from_tle(tle_data)

        # --- 3. Capa de Presentación ---
        print("\n📊 Paso 3: Renderizando simulación espacial...")
        visualizer = OrbitVisualizer()

        print(
            f"   -> Mostrando órbita de: {tle_data['name']} (Cierra la ventana para terminar)"
        )
        visualizer.plot_2d(orbit, name=tle_data["name"])

        print("\n✨ ¡Prueba de física orbital finalizada con éxito!")

    except SpaceToolkitError as e:
        print(f"\n❌ Error en el toolkit: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
