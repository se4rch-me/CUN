# Sistema de Registro de Comparendos — CUN

[![GitHub](https://img.shields.io/badge/GitHub-se4rch--me%2FCUN-181717?logo=github)](https://github.com/se4rch-me/CUN)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

Aplicación de escritorio para el registro y consulta de comparendos de tránsito,
desarrollada con Python + tkinter (UI nativa sin instalación adicional).

## Estructura del Proyecto

```
CUN/
├── main.py                  ← Punto de entrada
├── config.py                ← Rutas y constantes globales
├── requirements.txt         ← Dependencias
├── data/
│   └── comparendos.xlsx     ← Archivo generado automáticamente
├── models/
│   ├── __init__.py
│   └── comparendo.py        ← Clase Comparendo + validaciones
├── services/
│   ├── __init__.py
│   └── storage.py           ← Lectura/escritura Excel (pandas)
└── ui/
    ├── __init__.py
    ├── app.py               ← Ventana principal (tabs)
    ├── styles.py            ← Paleta de colores y fuentes
    └── widgets.py           ← Widgets reutilizables
```

## Requisitos

- Python **3.9** o superior (se incluye en macOS 12+ y Windows opcionalmente).
- `pip` disponible en el PATH.

## Instalación

```bash
# Clonar o copiar el proyecto
cd CUN/

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

### Interfaz gráfica (modo normal)
```bash
python main.py
```

### Modo consola (sin entorno gráfico)
```bash
python main.py --consola
```

## Compatibilidad

| Sistema         | UI gráfica | Modo consola |
|-----------------|:----------:|:------------:|
| macOS 10.15+    | ✅         | ✅           |
| Windows 10/11   | ✅         | ✅           |
| Windows 7/8     | ✅ *       | ✅           |
| Linux (X11)     | ✅         | ✅           |

> \* Windows 7/8 requiere instalar Python manualmente desde python.org.

## Datos guardados

El archivo `data/comparendos.xlsx` se crea automáticamente en el mismo directorio
del proyecto. No es necesario crearlo manualmente.

## Notas técnicas

- **Rutas**: se usan `pathlib.Path` para compatibilidad total entre sistemas operativos.
- **UI**: tkinter está incluido en la instalación estándar de Python (no requiere pip).
- **Persistencia**: pandas + openpyxl; los registros se acumulan sin borrar los anteriores.
- **Validación**: toda la lógica de validación vive en `models/comparendo.py`.
