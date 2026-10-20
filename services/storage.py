"""
services/storage.py
--------------------
Servicio de persistencia: lectura y escritura de comparendos
en el archivo Excel local usando pandas.

Toda la lógica de I/O está aquí, separada de la UI y del modelo.
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Optional

import pandas as pd

from config import COLUMNAS, EXCEL_FILE
from models.comparendo import Comparendo

# Suprimir FutureWarnings de pandas para no ensuciar la consola/logs
warnings.simplefilter(action="ignore", category=FutureWarning)


class StorageError(IOError):
    """Excepción personalizada para errores de almacenamiento."""


class ComparendoStorage:
    """
    Gestiona la persistencia de Comparendos en un archivo Excel.

    Parámetros
    ----------
    filepath : Path | str
        Ruta al archivo Excel. Por defecto usa EXCEL_FILE de config.
    """

    def __init__(self, filepath: Path | str = EXCEL_FILE) -> None:
        self.filepath = Path(filepath)

    # ------------------------------------------------------------------
    # Lectura
    # ------------------------------------------------------------------

    def _leer_dataframe(self) -> pd.DataFrame:
        """Lee el archivo Excel y devuelve un DataFrame con las columnas garantizadas."""
        if self.filepath.exists():
            try:
                df = pd.read_excel(self.filepath, dtype=str)
                # Asegurar que todas las columnas requeridas existan
                for col in COLUMNAS:
                    if col not in df.columns:
                        df[col] = ""
                return df[COLUMNAS]
            except Exception as e:
                raise StorageError(f"No se pudo leer el archivo Excel: {e}") from e
        return pd.DataFrame(columns=COLUMNAS)

    def obtener_numeros_existentes(self) -> list[str]:
        """
        Devuelve la lista de números de comparendo ya registrados.
        Útil para validar duplicados antes de mostrar el formulario.
        """
        try:
            df = self._leer_dataframe()
            if not df.empty and "Número Comparendo" in df.columns:
                return df["Número Comparendo"].dropna().astype(str).tolist()
        except StorageError:
            pass
        return []

    def obtener_todos(self) -> pd.DataFrame:
        """
        Devuelve el DataFrame completo con todos los comparendos registrados.
        Devuelve un DataFrame vacío si no hay datos.
        """
        try:
            return self._leer_dataframe()
        except StorageError:
            return pd.DataFrame(columns=COLUMNAS)

    def existe_numero(self, numero: int | str) -> bool:
        """Verifica si un número de comparendo ya está registrado."""
        return str(numero) in self.obtener_numeros_existentes()

    # ------------------------------------------------------------------
    # Escritura
    # ------------------------------------------------------------------

    def guardar(self, comparendo: Comparendo) -> None:
        """
        Agrega un Comparendo al archivo Excel sin borrar los existentes.

        Raises
        ------
        StorageError
            Si el número ya existe (duplicado) o si hay un error de escritura.
        """
        # Validación de duplicados
        if self.existe_numero(comparendo.numero):
            raise StorageError(
                f"El comparendo N° {comparendo.numero} ya existe en el archivo. "
                "No se guardará para evitar duplicados."
            )

        df = self._leer_dataframe()

        nuevo = pd.DataFrame([comparendo.a_dict()])
        df = pd.concat([df, nuevo], ignore_index=True)
        df = df[COLUMNAS]

        try:
            # Asegurar que el directorio padre exista (cross-platform)
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            df.to_excel(self.filepath, index=False)
        except PermissionError:
            raise StorageError(
                "No se pudo escribir en el archivo Excel. "
                "Asegúrese de que no está abierto en otro programa."
            )
        except Exception as e:
            raise StorageError(f"Error inesperado al guardar: {e}") from e

    # ------------------------------------------------------------------
    # Propiedades
    # ------------------------------------------------------------------

    @property
    def total_registros(self) -> int:
        """Número total de comparendos almacenados."""
        return len(self.obtener_todos())

    @property
    def ruta_str(self) -> str:
        """Representación legible de la ruta del archivo (cross-platform)."""
        return str(self.filepath)
