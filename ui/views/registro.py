"""
ui/views/registro.py
--------------------
Vista del formulario de registro de comparendos.

Expone `RegistroView`: un tk.Frame autónomo que recibe el storage
y un callback `on_guardado` para notificar a la ventana principal.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Callable

from config import TIPOS_DOCUMENTO
from models.comparendo import Comparendo, ComparendoError
from services.storage import ComparendoStorage, StorageError
from ui import styles as S
from ui.widgets import Button, CardFrame, EntryField, Label, StyledCombo

# Definición de campos: (etiqueta visible, clave interna)
_CAMPOS: list[tuple[str, str]] = [
    ("Número de Comparendo *",       "num_comp"),
    ("Tipo de Documento *",          "tipo_doc"),
    ("Identificación del Infractor *","id_inf"),
    ("Nombre Completo del Infractor *","nombre_inf"),
    ("Código de la Infracción *",    "cod_inf"),
    ("Valor de la Multa (COP) *",    "val_multa"),
]

_AYUDA = [
    "• Número Comparendo: solo dígitos.",
    "• Tipo Documento: CC, CE o NIT.",
    "• Identificación: solo dígitos.",
    "• Nombre: letras y espacios.",
    "• Infracción: código o descripción.",
    "• Valor Multa: número positivo.",
    "",
    "✓  Los registros se acumulan en el",
    "    archivo Excel sin borrar los anteriores.",
]


class RegistroView(tk.Frame):
    """
    Formulario de ingreso de un nuevo comparendo.

    Parámetros
    ----------
    master      : Widget padre (tab del Notebook).
    storage     : Instancia de ComparendoStorage para persistencia.
    on_guardado : Callable opcional; se invoca con el mensaje de éxito
                  tras guardar, para que la ventana principal actualice
                  su barra de estado.
    """

    def __init__(
        self,
        master: tk.Widget,
        storage: ComparendoStorage,
        on_guardado: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(master, bg=S.COLOR_BG)
        self.storage = storage
        self.on_guardado = on_guardado
        self._entries: dict[str, tk.Widget] = {}
        self._build()

    # ------------------------------------------------------------------
    # Construcción del layout
    # ------------------------------------------------------------------

    def _build(self) -> None:
        self.pack(fill="both", expand=True, padx=S.PAD_OUTER, pady=S.PAD_OUTER)

        Label(self, text="Nuevo Comparendo", title=True).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, S.PAD_INNER)
        )

        self._build_form(CardFrame(self))
        self._build_help(CardFrame(self))

    def _build_form(self, card: CardFrame) -> None:
        card.grid(row=1, column=0, sticky="nw")

        for i, (etiqueta, key) in enumerate(_CAMPOS):
            Label(card, text=etiqueta, muted=True).grid(
                row=i, column=0, sticky="w", pady=(S.PAD_WIDGET, 0)
            )
            widget = (
                self._make_combo(card) if key == "tipo_doc"
                else EntryField(card)
            )
            widget.grid(row=i, column=1, sticky="w", padx=(S.PAD_INNER, 0), pady=(S.PAD_WIDGET, 0))
            self._entries[key] = widget

        # Botones de acción
        btn_row = tk.Frame(card, bg=S.COLOR_SURFACE)
        btn_row.grid(row=len(_CAMPOS), column=0, columnspan=2, pady=(S.PAD_OUTER, 0), sticky="w")
        Button(btn_row, text="Guardar Comparendo", command=self._guardar).pack(side="left")
        Button(btn_row, text="Limpiar Campos",     command=self.limpiar).pack(side="left", padx=(S.PAD_WIDGET, 0))

    def _build_help(self, card: CardFrame) -> None:
        card.grid(row=1, column=1, sticky="nw", padx=(S.PAD_INNER, 0))
        Label(card, text="Instrucciones").pack(anchor="w")
        for linea in _AYUDA:
            Label(card, text=linea, muted=True, justify="left").pack(anchor="w")

    @staticmethod
    def _make_combo(parent: tk.Widget) -> StyledCombo:
        combo = StyledCombo(parent, values=TIPOS_DOCUMENTO)
        combo.current(0)
        return combo

    # ------------------------------------------------------------------
    # Lógica de negocio
    # ------------------------------------------------------------------

    def _guardar(self) -> None:
        """Valida, crea el Comparendo y lo persiste."""
        try:
            comparendo = Comparendo.desde_strings(
                numero        = self._entries["num_comp"].get(),
                tipo_doc      = self._entries["tipo_doc"].get(),
                identificacion= self._entries["id_inf"].get(),
                nombre        = self._entries["nombre_inf"].get(),
                infraccion    = self._entries["cod_inf"].get(),
                valor_multa   = self._entries["val_multa"].get(),
            )
        except ComparendoError as e:
            messagebox.showwarning("Campo inválido", str(e), parent=self)
            return

        try:
            self.storage.guardar(comparendo)
        except StorageError as e:
            messagebox.showerror("Error al guardar", str(e), parent=self)
            return

        total = self.storage.total_registros
        mensaje = f"✓  Comparendo N° {comparendo.numero} guardado. Total: {total} registro(s)."

        messagebox.showinfo(
            "Guardado exitoso",
            f"Comparendo N° {comparendo.numero} registrado.\nTotal en historial: {total} registro(s).",
            parent=self,
        )

        if self.on_guardado:
            self.on_guardado(mensaje)

        self.limpiar()

    def limpiar(self) -> None:
        """Restablece todos los campos a su estado inicial."""
        for key, widget in self._entries.items():
            if isinstance(widget, StyledCombo):
                widget.current(0)
            elif isinstance(widget, EntryField):
                widget.delete(0, "end")
