"""
ui/widgets.py
-------------
Widgets reutilizables y helpers de layout para la aplicación.
Todos los widgets heredan de sus contrapartes de tkinter/ttk y
aplican el tema centralizado de ui/styles.py.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from ui import styles as S


# ---------------------------------------------------------------------------
# Frame con borde simulado
# ---------------------------------------------------------------------------

class CardFrame(tk.Frame):
    """Frame con fondo de 'card' y padding estándar."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("bg", S.COLOR_SURFACE)
        kwargs.setdefault("padx", S.PAD_INNER)
        kwargs.setdefault("pady", S.PAD_INNER)
        super().__init__(master, **kwargs)


# ---------------------------------------------------------------------------
# Etiqueta estilizada
# ---------------------------------------------------------------------------

class Label(tk.Label):
    """Etiqueta con colores y fuente del tema."""

    def __init__(self, master, text: str = "", muted: bool = False, title: bool = False, **kwargs):
        font = S.FONT_TITLE if title else S.FONT_LABEL
        color = S.COLOR_TEXT_MUTED if muted else S.COLOR_TEXT
        kwargs.setdefault("bg", master.cget("bg"))
        kwargs.setdefault("fg", color)
        kwargs.setdefault("font", font)
        super().__init__(master, text=text, **kwargs)


# ---------------------------------------------------------------------------
# Campo de entrada
# ---------------------------------------------------------------------------

class EntryField(tk.Entry):
    """Entry con estilo dark."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("bg", S.COLOR_BG)
        kwargs.setdefault("fg", S.COLOR_TEXT)
        kwargs.setdefault("insertbackground", S.COLOR_TEXT)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("font", S.FONT_INPUT)
        kwargs.setdefault("width", S.ENTRY_WIDTH)
        kwargs.setdefault("highlightthickness", 1)
        kwargs.setdefault("highlightbackground", S.COLOR_BORDER)
        kwargs.setdefault("highlightcolor", S.COLOR_ACCENT)
        super().__init__(master, **kwargs)


# ---------------------------------------------------------------------------
# Combobox estilizado
# ---------------------------------------------------------------------------

class StyledCombo(ttk.Combobox):
    """Combobox con tema aplicado via ttk.Style."""

    _style_init = False

    def __init__(self, master, values: list[str], **kwargs):
        if not StyledCombo._style_init:
            _init_combo_style()
            StyledCombo._style_init = True

        kwargs.setdefault("state", "readonly")
        kwargs.setdefault("font", S.FONT_INPUT)
        kwargs.setdefault("width", S.ENTRY_WIDTH - 3)
        kwargs.setdefault("style", "Dark.TCombobox")
        super().__init__(master, values=values, **kwargs)


def _init_combo_style():
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Dark.TCombobox",
        fieldbackground=S.COLOR_BG,
        background=S.COLOR_SURFACE,
        foreground=S.COLOR_TEXT,
        selectforeground=S.COLOR_BTN_TEXT,      # oscuro — legible sobre selección gris
        selectbackground=S.COLOR_BTN_SECONDARY, # gris medio como resaltado de selección
        bordercolor=S.COLOR_BORDER,
        arrowcolor=S.COLOR_TEXT_MUTED,          # flecha visible pero discreta
    )


# ---------------------------------------------------------------------------
# Botón con hover
# ---------------------------------------------------------------------------

class Button(tk.Button):
    """
    Botón con tres variantes de color:
      - Normal   : fondo plateado claro  / texto oscuro  → máximo contraste
      - secondary: fondo gris medio      / texto oscuro
      - danger   : fondo rojo saturado   / texto blanco
    """

    def __init__(self, master, text: str, command=None,
                 danger: bool = False, secondary: bool = False, **kwargs):
        if danger:
            bg, bg_hover = S.COLOR_ERROR, S.COLOR_ERROR_HOVER
            fg = S.COLOR_BTN_TEXT_DANGER          # blanco sobre rojo
        elif secondary:
            bg, bg_hover = S.COLOR_BTN_SECONDARY, S.COLOR_BTN_SEC_HOVER
            fg = S.COLOR_BTN_TEXT                 # oscuro sobre gris medio
        else:
            bg, bg_hover = S.COLOR_ACCENT, S.COLOR_ACCENT_HOVER
            fg = S.COLOR_BTN_TEXT                 # oscuro sobre plateado

        kwargs.setdefault("bg", bg)
        kwargs.setdefault("fg", fg)
        kwargs.setdefault("activebackground", bg_hover)
        kwargs.setdefault("activeforeground", fg)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("font", S.FONT_BUTTON)
        kwargs.setdefault("width", S.BUTTON_WIDTH)
        kwargs.setdefault("cursor", "hand2")
        kwargs.setdefault("pady", 6)
        super().__init__(master, text=text, command=command, **kwargs)

        self._bg = bg
        self._bg_hover = bg_hover
        self.bind("<Enter>", lambda _: self.config(bg=self._bg_hover))
        self.bind("<Leave>", lambda _: self.config(bg=self._bg))



# ---------------------------------------------------------------------------
# Tabla de datos (Treeview)
# ---------------------------------------------------------------------------

class DataTable(tk.Frame):
    """Treeview estilizado con scrollbars para mostrar comparendos."""

    def __init__(self, master, columns: list[str], **kwargs):
        kwargs.setdefault("bg", S.COLOR_SURFACE)
        super().__init__(master, **kwargs)

        self._build_table(columns)

    def _build_table(self, columns: list[str]):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Dark.Treeview",
            background=S.COLOR_BG,
            foreground=S.COLOR_TEXT,
            fieldbackground=S.COLOR_BG,
            rowheight=26,
            font=S.FONT_TABLE,
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=S.COLOR_SURFACE,
            foreground=S.COLOR_TEXT_MUTED,   # gris claro: legible, no compite con botones
            font=(S.FONT_TABLE[0], S.FONT_TABLE[1], "bold"),
            relief="flat",
        )
        style.map("Dark.Treeview", background=[("selected", S.COLOR_BTN_SECONDARY)])

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            style="Dark.Treeview",
        )

        # Configurar columnas y encabezados
        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=140, minwidth=80)

        # Scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def cargar(self, filas: list[dict]):
        """Limpia e inserta nuevas filas en la tabla."""
        self.tree.delete(*self.tree.get_children())
        for fila in filas:
            valores = [fila.get(col, "") for col in self.tree["columns"]]
            self.tree.insert("", "end", values=valores)


# ---------------------------------------------------------------------------
# Barra de estado
# ---------------------------------------------------------------------------

class StatusBar(tk.Label):
    """Barra de estado en la parte inferior de la ventana."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("bg", S.COLOR_SURFACE)
        kwargs.setdefault("fg", S.COLOR_TEXT_MUTED)
        kwargs.setdefault("font", S.FONT_TABLE)
        kwargs.setdefault("anchor", "w")
        kwargs.setdefault("padx", S.PAD_INNER)
        super().__init__(master, **kwargs)

    def set(self, text: str, color: Optional[str] = None):
        self.config(text=text, fg=color or S.COLOR_TEXT_MUTED)

    def ok(self, text: str):
        self.set(text, S.COLOR_SUCCESS)

    def error(self, text: str):
        self.set(text, S.COLOR_ERROR)

    def warn(self, text: str):
        self.set(text, S.COLOR_WARNING)
