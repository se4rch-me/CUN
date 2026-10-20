"""
config.py
---------
Configuración global y rutas adaptables a cualquier sistema operativo
(Windows, macOS, Linux) usando pathlib para máxima compatibilidad.
"""

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# RUTAS BASE
# ---------------------------------------------------------------------------

# Directorio raíz del proyecto (donde vive este archivo)
BASE_DIR: Path = Path(__file__).resolve().parent

# Directorio de datos (se crea automáticamente si no existe)
DATA_DIR: Path = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Archivo principal de almacenamiento
EXCEL_FILE: Path = DATA_DIR / "comparendos.xlsx"

# ---------------------------------------------------------------------------
# COLUMNAS DEL MODELO
# ---------------------------------------------------------------------------

COLUMNAS = [
    "Número Comparendo",
    "Tipo Documento",
    "Identificación",
    "Nombre Infractor",
    "Infracción",
    "Valor Multa",
]

# ---------------------------------------------------------------------------
# TIPOS DE DOCUMENTO PERMITIDOS
# ---------------------------------------------------------------------------

TIPOS_DOCUMENTO = ["CC", "CE", "NIT"]

# ---------------------------------------------------------------------------
# META
# ---------------------------------------------------------------------------

APP_NAME = "Sistema de Registro de Comparendos"
APP_VERSION = "2.0.0"
