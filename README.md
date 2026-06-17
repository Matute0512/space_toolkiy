# 🌌 Space Toolkit

Un conjunto de herramientas de nivel profesional para el análisis de ciencia de datos astronómicos y la simulación astrodinámica. Construido con Python aplicando principios de Arquitectura Limpia y Programación Orientada a Objetos.

## 🚀 Características Principales (v1.0.0)

* **Extracción de Datos de Exoplanetas:** Conexión directa con la API TAP del NASA Exoplanet Archive con sistema de caché local.
* **Procesamiento y Análisis:** Limpieza de datos y filtrado matemático utilizando Pandas para identificar candidatos planetarios "Tipo Tierra".
* **Astrodinámica y Física Orbital:** Parseo y validación de datos TLE (Two-Line Element), resolución iterativa de la Ecuación de Kepler y conversión a parámetros keplerianos.
* **Visualización Científica:** Renderizado de órbitas 2D (ej. Estación Espacial Internacional) y gráficos de dispersión utilizando Matplotlib y Poliastro.

## 🏗️ Arquitectura del Proyecto

El sistema está diseñado aplicando el principio de Separación de Responsabilidades (SoC), dividido en módulos altamente cohesivos:

* `core/`: Capa transversal (Manejo de Excepciones, Logging, Configuración).
* `exoplanets/`: Pipeline de ciencia de datos (Loader, Analyzer, Visualizer).
* `orbits/`: Motor físico (TLE Parser, Physics Engine, Orbit Plotter).

## ⚙️ Instalación y Requisitos

Este proyecto utiliza **Poetry** para garantizar un entorno virtual determinista y libre de conflictos de dependencias.

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener Python 3.10 y Poetry instalados.
3. Instala el entorno y las dependencias ejecutando:
   ```bash
   poetry install
   ´´´