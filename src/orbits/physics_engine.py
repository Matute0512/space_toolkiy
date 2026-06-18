"""
Módulo de Motor Físico Orbital.

Capa de lógica de negocio responsable de traducir datos TLE crudos a
parámetros keplerianos y generar instancias de órbitas físicas utilizando
Poliastro y Astropy.
"""

import math
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Earth
from poliastro.twobody import Orbit

from ..core.logger import get_logger
from ..core.exceptions import OrbitCalculationError

logger = get_logger(__name__)


class PhysicsEngine:
    """Clase para cálculos astrodinámicos y propagación orbital."""

    def __init__(self):
        # Constante gravitacional de la Tierra (mu)
        self.mu = Earth.k.to(u.m**3 / u.s**2).value  # type: ignore
        logger.info("PhysicsEngine inicializado. Atrayente principal: La Tierra.")

    def solve_kepler(self, M: float, e: float, tol: float = 1e-8) -> float:
        """Resueve la ecuación de Kepler (M = E - e*sin(E)) iterativamente usando Newton-Raphson.

        Args:
            M (float): Anomalía Media en radianes.
            e (float): Excentricidad.
            tol (float, optional): Tolerancia del Error.

        Returns:
            float: Anomalía Excéntrica en radianes.
        """
        E = M if e < 0.8 else math.pi
        for _ in range(100):
            delta = (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
            E -= delta
            if abs(delta) < tol:
                break
        return E

    def true_anomaly_from_mean(self, M_deg: float, e: float) -> float:
        """Convierte Anomalía Media a Anomalía Verdadera

        Args:
            M_deg (float): Anomalía media en grados.
            e (float): Excentricidad orbital.

        Returns:
            float: Anomalía verdadera en radianes.
        """
        M_rad = math.radians(M_deg)
        E_rad = self.solve_kepler(M_rad, e)

        nu_rad = 2 * math.atan2(
            math.sqrt(1 + e) * math.sin(E_rad / 2),
            math.sqrt(1 - e) * math.cos(E_rad / 2),
        )
        return nu_rad

    def create_orbit_from_tle(self, tle_data: dict) -> Orbit:
        """Calcula los parámetros oritales clásicos a partir de un diccionario TLE.

        Args:
            tle_data (dict): Diccionario con las líneas validadas del TLE.

        Returns:
            Orbit: Objeto de Paliastro que representa la órbita.

        Raises:
            OrbitCalculationError: Si los datos son inválidos o el calculo falla.
        """
        try:
            line1 = tle_data["line1"]
            line2 = tle_data["line2"]
            name = tle_data["name"]

            # 1. Extracción basada en los índices exactos del formato TLE
            inc_deg = float(line2[8:16])
            raan_deg = float(line2[17:25])
            ecc = float("0." + line2[26:33].strip())
            argp_deg = float(line2[34:42])
            M_deg = float(line2[43:51])
            mean_motion_rev_day = float(line2[52:63])

            if ecc >= 1.0 or ecc < 0.0:
                raise OrbitCalculationError(
                    f"Excentricidad inválida {ecc} para órbita terrestre."
                )

            # 2. Resolver anomalía verdadera (De Matemática Pura a Geometría)
            nu_rad = self.true_anomaly_from_mean(M_deg, ecc)

            # 3. Conversión de Movimiento Medio (n) a Semieje Mayor (a)
            n_rad_s = mean_motion_rev_day * (2 * math.pi / 86400.0)
            a_meters = (self.mu / (n_rad_s**2)) ** (1 / 3)

            # 4. Extraer y formatear la Época (Tiempo) usando Matemática de Tiempos
            year_str = line1[18:20]
            day_str = line1[20:32]
            year_int = int(year_str)
            full_year = 2000 + year_int if year_int < 57 else 1900 + year_int

            day_float = float(day_str)

            # Creamos la fecha base: 1 de Enero de ese año
            base_time = Time(f"{full_year}-01-01T00:00:00", format="isot", scale="utc")

            # Le sumamos los días transcurridos (restamos 1 porque el 1 de Enero es el día 1, no el 0)
            epoch = base_time + (day_float - 1) * u.day  # type: ignore

            # 5. Instanciar la Órbita en Paliastro inyectando unidades astrofísicas
            orbit = Orbit.from_classical(
                attractor=Earth,
                a=a_meters * u.m,  # type: ignore
                ecc=ecc * u.one,  # type: ignore
                inc=inc_deg * u.deg,  # type: ignore
                raan=raan_deg * u.deg,  # type: ignore
                argp=argp_deg * u.deg,  # type: ignore
                nu=nu_rad * u.rad,  # type: ignore
                epoch=epoch,
            )

            logger.info(
                f"Órbita generada: '{name}'. Semieje Myor: {a_meters/1000:.2f} km."
            )
            return orbit

        except ValueError as e:
            logger.error("Error parseando los valores numéricos del TLE.")
            raise OrbitCalculationError(f"Datos TLE corruptos o ilegibles: {e}")
        except Exception as e:
            logger.error(f"Fallo en la resolución orbital: {e}")
            raise OrbitCalculationError(f"Cálculo físico fallido: {e}")
