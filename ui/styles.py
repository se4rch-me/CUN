"""
ui/styles.py
------------
Paleta de colores, fuentes y constantes de estilo para la UI.
Centralizar aquí permite cambiar el tema en un solo lugar.
"""

# ---------------------------------------------------------------------------
# PALETA PRINCIPAL
# ---------------------------------------------------------------------------

COLOR_BG = "#0F172A"          # Fondo general (azul muy oscuro)
COLOR_SURFACE = "#1E293B"     # Superficies (cards, frames)
COLOR_BORDER = "#334155"      # Bordes sutiles
COLOR_ACCENT = "#3B82F6"      # Azul primario (botones, selección)
COLOR_ACCENT_HOVER = "#2563EB"  # Hover del acento
COLOR_SUCCESS = "#22C55E"     # Verde éxito
COLOR_WARNING = "#F59E0B"     # Amarillo advertencia
COLOR_ERROR = "#EF4444"       # Rojo error
COLOR_TEXT = "#F1F5F9"        # Texto principal
COLOR_TEXT_MUTED = "#94A3B8"  # Texto secundario

# ---------------------------------------------------------------------------
# FUENTES
# ---------------------------------------------------------------------------

# tkinter usa tuplas (familia, tamaño, peso)
FONT_TITLE = ("Segoe UI", 20, "bold")      # Windows; fallback en macOS: San Francisco
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10)
FONT_INPUT = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 10, "bold")
FONT_TABLE = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 9)               # Monospace para rutas

# ---------------------------------------------------------------------------
# DIMENSIONES
# ---------------------------------------------------------------------------

PAD_OUTER = 24          # Margen exterior de la ventana
PAD_INNER = 12          # Padding interno de secciones
PAD_WIDGET = 6          # Espaciado entre widgets
ENTRY_WIDTH = 35        # Ancho en caracteres de los campos de entrada
BUTTON_WIDTH = 18       # Ancho en caracteres de los botones principales
CORNER_RADIUS = 8       # Radio de bordes (no nativo en tkinter estándar, referencial)
