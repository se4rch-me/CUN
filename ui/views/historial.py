"""
ui/views/historial.py
---------------------
Vista de consulta del historial de comparendos.

Expone `HistorialView`: un tk.Frame autónomo que muestra la tabla
de registros y permite actualizarla desde el archivo Excel.
"""

from __future__ import annotations

import tkinter as tk
from typing import Callable

from config import COLUMNAS
from services.storage import ComparendoStorage
from ui import styles as S
from ui.widgets import Button, DataTable, Label


class HistorialView(tk.Frame):
    """
    Tabla scrolleable con todos los comparendos registrados.

    Parámetros
    ----------
    master       : Widget padre (tab del Notebook).
    storage      : Instancia de ComparendoStorage para leer los datos.
    on_actualizado: Callable opcional; recibe el mensaje de estado tras
                   cada actualización (para la StatusBar de la App).
    """

    def __init__(
        self,
        master: tk.Widget,
        storage: ComparendoStorage,
        on_actualizado: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(master, bg=S.COLOR_BG)
        self.storage = storage
        self.on_actualizado = on_actualizado
        self._build()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build(self) -> None:
        self.pack(fill="both", expand=True, padx=S.PAD_OUTER, pady=S.PAD_OUTER)

        # Encabezado con título y botón
        header = tk.Frame(self, bg=S.COLOR_BG)
        header.pack(fill="x", pady=(0, S.PAD_INNER))

        Label(header, text="Historial de Comparendos", title=True).pack(side="left")
        Button(header, text="↻  Actualizar", command=self.actualizar, width=14).pack(side="right")

        # Tabla principal
        self.tabla = DataTable(self, columns=COLUMNAS)
        self.tabla.pack(fill="both", expand=True)

        # Conteo de registros
        self.lbl_conteo = Label(self, text="", muted=True)
        self.lbl_conteo.pack(anchor="e", pady=(S.PAD_WIDGET, 0))

    # ------------------------------------------------------------------
    # Lógica
    # ------------------------------------------------------------------

    def actualizar(self) -> None:
        """Recarga desde disco y refresca la tabla."""
        df = self.storage.obtener_todos()
        self.tabla.cargar(df.to_dict(orient="records"))
        n = len(df)
        self.lbl_conteo.config(text=f"{n} comparendo(s) registrado(s).")

        if self.on_actualizado:
            self.on_actualizado(f"Historial actualizado — {n} registro(s).")
