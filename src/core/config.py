"""
Módulo de Configuración.

Centraliza las constantes globales, URLs de APIs externas y rutas de directorios
para el Toolkit Espacial. Evita el uso de valores "mágicos" (hardcoded) en la lógica de negocio.
"""

from pathlib import Path

# ==========================================
# 1. CONFIGURACIÓN DE RUTAS (PATHS)
# ==========================================

# Resuelve dinámicamente la raíz del proyecto (3 niveles arriba desde src/core/config.py)
# Esto garantiza que las rutas funcionen sin importar desde dónde se ejecute el script.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Directorio destinado a almacenar archivos CSV O JSON temporales
DATA_DIR = BASE_DIR/"data"

# Ruta especifica para guardar el caché de los exoplanetas
EXOPLANET_CACHE_FILE: Path = DATA_DIR / "nasa_exoplanets.csv"

# ==========================================
# 2. CONFIGURACIÓN DE APIS Y RED
# ==========================================

# URL del servicio TAP (Table Access Protocol) del NASA Exoplanet Archive
NASA_EXOPLANET_TAP_URL: str = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# Tiempo máximo de espera para las conexiones de red (en segundos)
# Previene que la aplicación se congele si la NASA está en mantenimiento
NETWORK_TIMEOUT: int = 30


# ==========================================
# 3. CONSTANTES FÍSICAS Y CIENTÍFICAS
# ==========================================
# Nota: La mayoría de constantes físicas de alta precisión serán proveídas
# directamente por `astropy.constants`, pero podemos agregar configuraciones
# de visualización o límites matemáticos aquí si el proyecto lo requiere más adelante.
