# 🌌 Space Toolkit (v2.0.0)

Un conjunto de herramientas de nivel profesional para el análisis de ciencia de datos astronómicos y la simulación astrodinámica. Construido con Python aplicando Arquitectura Limpia, POO y visualización científica interactiva.

## 🚀 Características Principales

* **Dashboard Interactivo:** Interfaz web completa construida con `Streamlit` para análisis en tiempo real.
* **Módulo de Exoplanetas:** * Conexión a la API TAP del NASA Exoplanet Archive.
  * Cálculo matemático del **Índice de Similitud con la Tierra (ESI)**.
  * Gráficos interactivos filtrables utilizando `Plotly`.
* **Motor de Astrodinámica:**
  * Parseo y validación de datos TLE (Two-Line Element).
  * Resolución de la Ecuación de Kepler y propagación de órbitas.
  * Renderizado **3D interactivo** de satélites orbitando la Tierra con control de colores.
* **Calidad de Software:** Sistema de pruebas unitarias automatizadas implementado con `pytest`.

## 🏗️ Arquitectura del Proyecto

El sistema está diseñado aplicando el principio de Separación de Responsabilidades (SoC):
* `core/`: Capa transversal (Manejo de Excepciones, Logging, Configuración).
* `exoplanets/`: Pipeline de ciencia de datos (Loader, Analyzer).
* `orbits/`: Motor físico (TLE Parser, Physics Engine, Orbit Visualizer).
* `ui/`: Interfaz de usuario y presentación (Streamlit Dashboard).

## ⚙️ Instalación y Uso

Este proyecto utiliza **Poetry** para garantizar un entorno virtual determinista.

1. Clona este repositorio y asegúrate de tener Python 3.10 y Poetry instalados.
2. Instala el entorno y las dependencias:
   ```bash
   poetry install