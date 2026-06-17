"""
Módulo de Excepciones.

Define la jerarquia de errores personalizados para el Toolkit Espacial.
Permite un manejo de errores detallado, predecible y robusto en toda la app.
"""


class SpaceToolkitError(Exception):
    """
    Clase base para todas las excepciones del toolkit.
    Cualquier error específico del proyecto heredará de esta clase.
    """

    pass


# --- Excepciones del Módulo de Ciencia de Datos (Exoplanetas) ---


class DataDownloadError(SpaceToolkitError):
    """Lanzada cuando falla la descarga o conexión con fuentes de datos externas (ej. NASA)"""

    pass


class DataValidationError(SpaceToolkitError):
    """Lanzada cuando los datos cargados no tienen el formato, tipos o columnas esperadas."""

    pass


# --- Excepciones del Módulo de Simulación Física (Órbitas) ---


class OrbitCalculationError(SpaceToolkitError):
    """Lanzada cuando un cálculo físico o de propagación orbital resulta inválido o infinito."""

    pass


class TLEParseError(SpaceToolkitError):
    """Lanzada cuando los datos de formato TLE (Two-Line Element) están corruptos o mal formateados."""

    pass
