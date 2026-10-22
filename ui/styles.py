"""
ui/styles.py
------------
Paleta de colores, fuentes y constantes de estilo para la UI.
Centralizar aquí permite cambiar el tema en un solo lugar.
"""

# ---------------------------------------------------------------------------
# PALETA PRINCIPAL — tema gris neutro
# ---------------------------------------------------------------------------

COLOR_BG      = "#1C1C1E"   # Fondo general (gris antracita)
COLOR_SURFACE = "#2C2C2E"   # Superficies: cards, frames, header
COLOR_BORDER  = "#48484A"   # Bordes sutiles

COLOR_ACCENT       = "#3A3F4B"   # Botón primario: gris-azulado oscuro
COLOR_ACCENT_HOVER = "#4A5160"   # Hover del botón primario
COLOR_SUCCESS = "#4CAF50"        # Verde apagado (estado OK)
COLOR_WARNING = "#C9912A"        # Ámbar oscuro (advertencia)
COLOR_ERROR   = "#7A2828"        # Burdeos (botón peligro / error)

COLOR_TEXT       = "#FFFFFF"     # Texto sobre fondos oscuros
COLOR_TEXT_MUTED = "#AEAEB2"     # Texto secundario (labels, ayuda)

# Texto sobre botones — siempre blanco para garantizar legibilidad
COLOR_BTN_TEXT = "#FFFFFF"

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
