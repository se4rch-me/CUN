"""
main.py
-------
Punto de entrada del Sistema de Registro de Comparendos.

Uso:
    python main.py              → lanza la interfaz gráfica (por defecto)
    python main.py --consola   → lanza el modo consola sin UI

Compatibilidad: Python 3.9+ | Windows | macOS | Linux
"""

from __future__ import annotations

import sys


def _lanzar_ui() -> None:
    """Inicializa el storage y arranca la ventana principal de tkinter."""
    # Importaciones diferidas para no penalizar el arranque en modo consola
    from services.storage import ComparendoStorage
    from ui.app import App

    storage = ComparendoStorage()
    app = App(storage)
    app.mainloop()


def _lanzar_consola() -> None:
    """Modo consola heredado del código original (útil sin entorno gráfico)."""
    from config import EXCEL_FILE
    from models.comparendo import Comparendo, ComparendoError
    from services.storage import ComparendoStorage, StorageError

    storage = ComparendoStorage()

    print("=" * 55)
    print("   SISTEMA DE REGISTRO DE COMPARENDOS  (modo consola)")
    print("=" * 55)
    print(f"Archivo Excel activo en: {storage.ruta_str}\n")

    existentes = storage.obtener_numeros_existentes()

    # ── Número de comparendo ──
    while True:
        num = input("Ingrese el N° de Comparendo (solo números): ").strip()
        if not num:
            print("[ALERTA]: No puede estar vacío.")
            continue
        if not num.isdigit():
            print("[ALERTA]: Solo se permiten dígitos.")
            continue
        if num in existentes:
            print(f"[ALERTA]: El comparendo N° {num} ya está registrado.")
            continue
        break

    # ── Tipo de documento ──
    from config import TIPOS_DOCUMENTO
    while True:
        tipo = input(f"Tipo de Documento {TIPOS_DOCUMENTO}: ").strip().upper()
        if tipo not in TIPOS_DOCUMENTO:
            print(f"[ALERTA]: Debe ser {', '.join(TIPOS_DOCUMENTO)}.")
            continue
        break

    # ── Identificación ──
    while True:
        id_inf = input("Identificación del Infractor (solo números): ").strip()
        if not id_inf.isdigit():
            print("[ALERTA]: Solo se permiten dígitos.")
            continue
        break

    # ── Nombre ──
    while True:
        nombre = input("Nombre Completo del Infractor: ").strip()
        sin_espacios = nombre.replace(" ", "")
        if not sin_espacios:
            print("[ALERTA]: No puede estar vacío.")
            continue
        # Permitir letras con tildes
        normalizado = sin_espacios.lower()
        for ch in "áéíóúüñ":
            normalizado = normalizado.replace(ch, "a")
        if not normalizado.isalpha():
            print("[ALERTA]: Solo letras y espacios.")
            continue
        break

    # ── Infracción ──
    while True:
        inf = input("Código / Descripción de la Infracción: ").strip()
        if not inf:
            print("[ALERTA]: No puede estar vacío.")
            continue
        break

    # ── Valor multa ──
    while True:
        val_str = input("Valor de la Multa (COP, solo números): ").strip().replace(",", ".")
        try:
            val = float(val_str)
            if val <= 0:
                raise ValueError
            break
        except ValueError:
            print("[ALERTA]: Debe ser un número positivo.")

    # ── Guardar ──
    try:
        comparendo = Comparendo.desde_strings(num, tipo, id_inf, nombre, inf, str(val))
        storage.guardar(comparendo)
        print(f"\n[ÉXITO]: Comparendo N° {num} guardado. Total: {storage.total_registros} registro(s).")
    except (ComparendoError, StorageError) as e:
        print(f"\n[ERROR]: {e}")
        sys.exit(1)

    # ── Mostrar historial ──
    df = storage.obtener_todos()
    print(f"\n--- HISTORIAL COMPLETO ({len(df)} registros) ---")
    print(df.to_string(index=False))


# ---------------------------------------------------------------------------
# Arranque
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if "--consola" in sys.argv:
        _lanzar_consola()
    else:
        _lanzar_ui()
