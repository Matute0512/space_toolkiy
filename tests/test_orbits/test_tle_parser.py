"""
Pruebas unitarias para el módulo de Astrodinámica (Órbitas).
"""

import pytest
from src.orbits.tle_parser import TLEParser
from src.core.exceptions import SpaceToolkitError


def test_parse_valid_tle():
    """Verifica que el parser pueda extraer correctamente los datos de un TLE válido."""

    # 1. Arrange: TLE real de la Estación Espacial Internacional
    valid_tle = (
        "ISS (ZARYA)\n"
        "1 25544U 98067A   23272.53177699  .00015569  00000-0  28172-3 0  9994\n"
        "2 25544  51.6415 141.0505 0005703  26.0441 334.0838 15.49479361418197"
    )
    parser = TLEParser()

    # 2. Act: Parseamos el string
    result = parser.parse_tle(valid_tle)

    # 3. Assert: Validamos la extracción
    assert (
        result["name"] == "ISS (ZARYA)"
    ), "No se extrajo correctamente el nombre del satélite."
    assert result["line1"].startswith(
        "1 25544U"
    ), "La primera línea del TLE no coincide."
    assert result["line2"].startswith(
        "2 25544"
    ), "La segunda línea del TLE no coincide."


def test_parse_invalid_tle_raises_error():
    """Verifica que el parser lance nuestra excepción personalizada si el TLE está roto."""

    # Arrange: TLE verdaderamente inválido (la línea 2 tiene menos de 69 caracteres)
    invalid_tle = (
        "ISS (ZARYA)\n"
        "1 25544U 98067A   23272.53177699  .00015569  00000-0  28172-3 0  9994\n"
        "2 25544  51.6415 141.0505 0005703  26.0441"  # <- Faltan datos aquí
    )
    parser = TLEParser()

    # Act & Assert: Ahora sí, al no tener 69 caracteres, el parser DEBE quejarse
    # y lanzar SpaceToolkitError (o su clase hija TLEParseError)
    with pytest.raises(SpaceToolkitError):
        parser.parse_tle(invalid_tle)
