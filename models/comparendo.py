"""
models/comparendo.py
--------------------
Clase de datos que representa un Comparendo.
Incluye validación de cada campo y conversión a diccionario.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from config import TIPOS_DOCUMENTO


class ComparendoError(ValueError):
    """Excepción personalizada para errores de validación de Comparendo."""


@dataclass
class Comparendo:
    """
    Representa un registro de comparendo de tránsito.

    Atributos
    ---------
    numero       : Número único del comparendo (entero positivo).
    tipo_doc     : Tipo de documento (CC, CE, NIT).
    identificacion: Número de identificación del infractor (entero positivo).
    nombre       : Nombre completo del infractor (solo letras y espacios).
    infraccion   : Código o descripción de la infracción cometida.
    valor_multa  : Valor monetario de la multa (número positivo).
    """

    TIPOS_DOC_VALIDOS: ClassVar[list[str]] = TIPOS_DOCUMENTO

    numero: int
    tipo_doc: str
    identificacion: int
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

        # --- Identificación ---
        identificacion = identificacion.strip()
        if not identificacion.isdigit():
            raise ComparendoError("La identificación debe contener únicamente dígitos.")

        # --- Nombre ---
        nombre = nombre.strip()
        nombre_sin_espacios = nombre.replace(" ", "")
        if not nombre_sin_espacios:
            raise ComparendoError("El nombre del infractor no puede estar vacío.")
        if not nombre_sin_espacios.replace("á", "a").replace("é", "e").replace("í", "i") \
                                  .replace("ó", "o").replace("ú", "u").replace("ñ", "n").isalpha():
            raise ComparendoError("El nombre debe contener únicamente letras y espacios.")

        # --- Infracción ---
        infraccion = infraccion.strip()
        if not infraccion:
            raise ComparendoError("El código de infracción no puede estar vacío.")

        # --- Valor multa ---
        valor_multa = valor_multa.strip().replace(",", ".")
        try:
            valor_num = float(valor_multa)
            if valor_num <= 0:
                raise ValueError
        except ValueError:
            raise ComparendoError("El valor de la multa debe ser un número positivo.")

        return cls(
            numero=int(numero),
            tipo_doc=tipo_doc,
            identificacion=int(identificacion),
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
            "Tipo Documento": self.tipo_doc,
            "Identificación": self.identificacion,
            "Nombre Infractor": self.nombre,
            "Infracción": self.infraccion,
            "Valor Multa": self.valor_multa,
        }

    def __str__(self) -> str:
        return (
            f"Comparendo #{self.numero} | {self.tipo_doc} {self.identificacion} "
            f"| {self.nombre} | {self.infraccion} | ${self.valor_multa:,.2f}"
        )
