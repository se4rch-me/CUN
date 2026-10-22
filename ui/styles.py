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

# Botones: fondo CLARO sobre fondo oscuro → contraste garantizado
COLOR_ACCENT        = "#D1D1D6"   # Botón primario: gris plateado claro
COLOR_ACCENT_HOVER  = "#E5E5EA"   # Hover: aún más claro
COLOR_BTN_SECONDARY = "#8E8E93"   # Botón secundario: gris medio
COLOR_BTN_SEC_HOVER = "#A0A0A8"   # Hover secundario
COLOR_ERROR         = "#962B2B"   # Rojo más saturado para botón peligro
COLOR_ERROR_HOVER   = "#B23333"

# Texto sobre botones primario/secundario → oscuro (contrasta sobre fondo claro)
COLOR_BTN_TEXT      = "#1C1C1E"   # Negro sobre plateado/gris claro
COLOR_BTN_TEXT_DANGER = "#FFFFFF" # Blanco sobre rojo

# Colores de estado (barra de estado)
COLOR_SUCCESS = "#4CAF50"   # Verde éxito
COLOR_WARNING = "#C9912A"   # Ámbar advertencia

COLOR_TEXT       = "#FFFFFF"   # Texto general sobre fondos oscuros
COLOR_TEXT_MUTED = "#AEAEB2"  # Texto secundario

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
