"""
Script temporal para probar la descarga de datos de la NASA.
"""

from src.exoplanets.data_loader import ExoplanetDataLoader
from src.core.exceptions import SpaceToolkitError


def main():
    print("🚀 Iniciando prueba de conexión con la NASA...\n")

    loader = ExoplanetDataLoader()

    try:
        # Esto desencadenará la descarga y la carga en Pandas
        df = loader.load_data()

        print("\n✨ ¡Éxito! Aquí tienes un vistazo a los datos:")
        # Mostramos solo las primeras 5 filas y algunas columnas clave
        print(df[['pl_name', 'hostname', 'discoverymethod', 'disc_year']].head())

    except SpaceToolkitError as e:
        print(f"\n❌ Algo falló en nuestro toolkit: {e}")


if __name__ == "__main__":
    main()
