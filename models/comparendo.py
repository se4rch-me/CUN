"""
models/comparendo.py
--------------------
Clase de datos que representa un Comparendo.
Incluye validación de cada campo según las reglas colombianas para cada
tipo de documento, y conversión a diccionario para persistencia.

Reglas de identificación por tipo de documento (Colombia):
  CC  (Cédula de Ciudadanía)  : 6–10 dígitos, solo numérico.
  CE  (Cédula de Extranjería) : 4–11 dígitos, solo numérico
                                (Migración Colombia, sin letras ni guiones).
  NIT (Nit tributario DIAN)   : 5–10 dígitos base + guion opcional + 1 dígito
                                de verificación. Ej: 900123456-7 o 9001234567.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar

from config import TIPOS_DOCUMENTO


class ComparendoError(ValueError):
    """Excepción personalizada para errores de validación de Comparendo."""


# ---------------------------------------------------------------------------
# Reglas de identificación por tipo de documento
# ---------------------------------------------------------------------------

_REGLAS_ID: dict[str, dict] = {
    "CC": {
        "patron":  re.compile(r"^\d{6,10}$"),
        "mensaje": "CC: debe contener entre 6 y 10 dígitos numéricos.",
    },
    "CE": {
        "patron":  re.compile(r"^\d{4,11}$"),
        "mensaje": "CE: debe contener entre 4 y 11 dígitos numéricos (sin letras ni guiones).",
    },
    "NIT": {
        # Formato: 5-10 dígitos base, con guion y dígito de verificación opcionales.
        # Ejemplos válidos: 900123456-7  |  9001234567  |  12345-6
        "patron":  re.compile(r"^\d{5,10}(-\d)?$"),
        "mensaje": "NIT: formato esperado XXXXXXXXX o XXXXXXXXX-X (guion y dígito de verificación opcionales).",
    },
}


@dataclass
class Comparendo:
    """
    Representa un registro de comparendo de tránsito.

    Atributos
    ---------
    numero        : Número único del comparendo (entero positivo).
    tipo_doc      : Tipo de documento (CC, CE, NIT).
    identificacion: Número/texto de identificación — str para preservar el guion del NIT.
    nombre        : Nombre completo del infractor (solo letras y espacios).
    infraccion    : Código o descripción de la infracción cometida.
    valor_multa   : Valor monetario de la multa (número positivo).
    """

    TIPOS_DOC_VALIDOS: ClassVar[list[str]] = TIPOS_DOCUMENTO

    numero: int
    tipo_doc: str
    identificacion: str   # str para conservar el formato NIT con guion
    nombre: str
    infraccion: str
    valor_multa: float

    # -----------------------------------------------------------------------
    # Constructor alternativo (desde strings crudos)
    # -----------------------------------------------------------------------

    @classmethod
    def desde_strings(
        cls,
        numero: str,
        tipo_doc: str,
        identificacion: str,
        nombre: str,
        infraccion: str,
        valor_multa: str,
    ) -> "Comparendo":
        """
        Crea un Comparendo validando y convirtiendo strings de entrada.
        Lanza ComparendoError con mensaje descriptivo si algún campo es inválido.
        """
        # --- Número de comparendo ---
        numero = numero.strip()
        if not numero:
            raise ComparendoError("El número de comparendo no puede estar vacío.")
        if not numero.isdigit():
            raise ComparendoError("El número de comparendo debe contener únicamente dígitos.")

        # --- Tipo de documento ---
        tipo_doc = tipo_doc.strip().upper()
        if tipo_doc not in cls.TIPOS_DOC_VALIDOS:
            raise ComparendoError(
                f"Tipo de documento inválido. Opciones válidas: {', '.join(cls.TIPOS_DOC_VALIDOS)}."
            )

        # --- Identificación (validación específica por tipo) ---
        identificacion = identificacion.strip()
        regla = _REGLAS_ID[tipo_doc]
        if not regla["patron"].match(identificacion):
            raise ComparendoError(regla["mensaje"])

        # --- Nombre ---
        nombre = nombre.strip()
        nombre_normalizado = (
            nombre.replace(" ", "")
                  .lower()
                  .replace("á", "a").replace("é", "e").replace("í", "i")
                  .replace("ó", "o").replace("ú", "u").replace("ü", "u")
                  .replace("ñ", "n")
        )
        if not nombre_normalizado:
            raise ComparendoError("El nombre del infractor no puede estar vacío.")
        if not nombre_normalizado.isalpha():
            raise ComparendoError("El nombre debe contener únicamente letras y espacios.")

        # --- Infracción ---
        infraccion = infraccion.strip()
        if not infraccion:
            raise ComparendoError("El código de infracción no puede estar vacío.")

        # --- Valor multa ---
        valor_multa_str = valor_multa.strip().replace(",", ".")
        try:
            valor_num = float(valor_multa_str)
            if valor_num <= 0:
                raise ValueError
        except ValueError:
            raise ComparendoError("El valor de la multa debe ser un número positivo.")

        return cls(
            numero=int(numero),
            tipo_doc=tipo_doc,
            identificacion=identificacion,   # se guarda tal como se ingresó
            nombre=nombre,
            infraccion=infraccion,
            valor_multa=valor_num,
        )

    # -----------------------------------------------------------------------
    # Serialización
    # -----------------------------------------------------------------------

    def a_dict(self) -> dict:
        """Devuelve el comparendo como diccionario alineado con las columnas Excel."""
        return {
            "Número Comparendo": self.numero,
            "Tipo Documento":    self.tipo_doc,
            "Identificación":    self.identificacion,
            "Nombre Infractor":  self.nombre,
            "Infracción":        self.infraccion,
            "Valor Multa":       self.valor_multa,
        }

    def __str__(self) -> str:
        return (
            f"Comparendo #{self.numero} | {self.tipo_doc} {self.identificacion} "
            f"| {self.nombre} | {self.infraccion} | ${self.valor_multa:,.2f}"
        )
