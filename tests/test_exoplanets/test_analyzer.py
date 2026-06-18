"""
Pruebas unitarias para el módulo de análisis de Exoplanetas.
"""

import pandas as pd
import pytest
from src.exoplanets.analyzer import ExoplanetAnalyzer


def test_calculate_esi_perfect_earth():
    """
    Verifica que el cálculo del Índice de Similitud con la Tierra (ESI)
    sea matemáticamente correcto para un planeta idéntico a la Tierra.
    """
    # 1. PREPARACIÓN (Arrange): Creamos datos simulados (Mock data)
    mock_data = pd.DataFrame(
        {
            "pl_name": ["Júpiter Caliente", "Tierra Perfecta", "Planeta Roto"],
            "hostname": ["Estrella X", "Sol 2.0", "Estrella Y"],
            # Masas (None para simular datos faltantes)
            "pl_bmasse": [317.8, 1.0, None],
            "pl_rade": [11.2, 1.0, 1.5],  # Radios
            "discoverymethod": ["Radial Velocity", "Transit", "Transit"],
        }
    )

    analyzer = ExoplanetAnalyzer(mock_data)

    # 2. ACCIÓN (Act): Ejecutamos la función que queremos probar
    result_df = analyzer.calculate_esi()

    # 3. VERIFICACIÓN (Assert): Comprobamos los resultados

    # El planeta con datos faltantes (None) debe haber sido eliminado (dropna)
    assert len(result_df) == 2, "El analizador no filtró correctamente los datos nulos."

    # Extraemos el valor ESI calculado para nuestra 'Tierra Perfecta'
    earth_esi = result_df.loc[
        result_df["pl_name"] == "Tierra Perfecta", "esi_score"
    ].values[0]

    # Validamos la matemática: Masa 1.0 y Radio 1.0 DEBEN dar un ESI de 1.0
    # Usamos pytest.approx por los problemas de precisión de los decimales (floats)
    assert earth_esi == pytest.approx(
        1.0
    ), f"El ESI esperado era 1.0, pero se obtuvo {earth_esi}"

    # Validamos el ordenamiento (El mayor ESI debe estar en la fila 0)
    assert (
        result_df.iloc[0]["pl_name"] == "Tierra Perfecta"
    ), "El DataFrame no se ordenó de mayor a menor ESI."
