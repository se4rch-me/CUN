"""
ui/app.py
---------
Ventana principal: solo orquesta el layout, el tema y los tabs.
Toda la lógica de cada sección vive en ui/views/.
"""

from __future__ import annotations

import platform
import tkinter as tk
import tkinter.ttk as ttk

from config import APP_NAME, APP_VERSION
from services.storage import ComparendoStorage
from ui import styles as S
from ui.widgets import StatusBar
from ui.views.registro import RegistroView
from ui.views.historial import HistorialView


class App(tk.Tk):
    """Ventana raíz: configura la ventana, aplica el tema y ensambla los tabs."""

    def __init__(self, storage: ComparendoStorage) -> None:
        super().__init__()
        self.storage = storage
        self._configurar_ventana()
        self._aplicar_tema()
        self._construir_ui()

    # ------------------------------------------------------------------
    # Configuración de la ventana
    # ------------------------------------------------------------------

    def _configurar_ventana(self) -> None:
        self.title(f"{APP_NAME}  v{APP_VERSION}")
        self.configure(bg=S.COLOR_BG)
        self.resizable(True, True)
        ancho, alto = 900, 660
        x = (self.winfo_screenwidth()  - ancho) // 2
        y = (self.winfo_screenheight() - alto)  // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.minsize(720, 520)
        if platform.system() == "Windows":
            try:
                self.iconbitmap(default="")
            except Exception:
                pass

    def _aplicar_tema(self) -> None:
        """Registra estilos ttk globales (Notebook y sus tabs)."""
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Dark.TNotebook", background=S.COLOR_BG, borderwidth=0, tabmargins=[2, 5, 2, 0])
        style.configure("Dark.TNotebook.Tab", background=S.COLOR_SURFACE,
                        foreground=S.COLOR_TEXT_MUTED, font=S.FONT_LABEL, padding=[16, 8])
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", S.COLOR_BG)],
                  foreground=[("selected", S.COLOR_ACCENT)])

    # ------------------------------------------------------------------
    # Ensamblado de la UI
    # ------------------------------------------------------------------

    def _construir_ui(self) -> None:
        self._construir_header()
        tk.Frame(self, bg=S.COLOR_BORDER, height=1).pack(fill="x")
        self._construir_notebook()
        tk.Frame(self, bg=S.COLOR_BORDER, height=1).pack(fill="x", pady=(S.PAD_INNER, 0))
        self._construir_statusbar()

    def _construir_header(self) -> None:
        header = tk.Frame(self, bg=S.COLOR_SURFACE, pady=S.PAD_INNER)
        header.pack(fill="x")
        tk.Label(header, text="🚦  " + APP_NAME,
                 bg=S.COLOR_SURFACE, fg=S.COLOR_TEXT, font=S.FONT_TITLE).pack(side="left", padx=S.PAD_OUTER)
        tk.Label(header, text=f"v{APP_VERSION}  •  {platform.system()} {platform.release()}",
                 bg=S.COLOR_SURFACE, fg=S.COLOR_TEXT_MUTED, font=S.FONT_SUBTITLE).pack(side="right", padx=S.PAD_OUTER)

    def _construir_notebook(self) -> None:
        nb = ttk.Notebook(self, style="Dark.TNotebook")
        nb.pack(fill="both", expand=True, padx=S.PAD_OUTER, pady=(S.PAD_INNER, 0))

        # Tab 1 — Registro
        frame_reg = tk.Frame(nb, bg=S.COLOR_BG)
        nb.add(frame_reg, text="  ➕  Registrar Comparendo  ")
        self._vista_registro = RegistroView(
            frame_reg, self.storage,
            on_guardado=lambda msg: self.status.ok(msg),
        )

        # Tab 2 — Historial
        frame_hist = tk.Frame(nb, bg=S.COLOR_BG)
        nb.add(frame_hist, text="  📋  Historial  ")
        self._vista_historial = HistorialView(
            frame_hist, self.storage,
            on_actualizado=lambda msg: self.status.set(msg),
        )

        nb.bind("<<NotebookTabChanged>>",
                lambda e: self._vista_historial.actualizar()
                if nb.index(nb.select()) == 1 else None)

    def _construir_statusbar(self) -> None:
        self.status = StatusBar(self)
        self.status.pack(fill="x", ipady=4)
        self.status.set(f"Archivo activo: {self.storage.ruta_str}")
