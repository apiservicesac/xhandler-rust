from dataclasses import dataclass, field
from datetime import date, time
from decimal import Decimal
from typing import Optional, List, Dict

from .common import (
    Proveedor, Cliente, Firmante, Detraccion, Percepcion, Direccion, FormaDePago,
    Anticipo, Descuento, Detalle, TotalImporteInvoice, TotalImpuestos, Guia,
    DocumentoRelacionado
)


@dataclass
class Invoice:
    proveedor: Proveedor
    cliente: Cliente

    leyendas: Dict[str, str] = field(default_factory=dict)
    serie_numero: str = ""
    moneda: Optional[str] = None
    fecha_emision: Optional[date] = None
    hora_emision: Optional[time] = None
    fecha_vencimiento: Optional[date] = None
    firmante: Optional[Firmante] = None
    icb_tasa: Optional[Decimal] = None
    igv_tasa: Optional[Decimal] = None
    ivap_tasa: Optional[Decimal] = None

    tipo_comprobante: Optional[str] = None
    tipo_operacion: Optional[str] = None

    detraccion: Optional[Detraccion] = None
    percepcion: Optional[Percepcion] = None

    direccion_entrega: Optional[Direccion] = None
    forma_de_pago: Optional[FormaDePago] = None

    anticipos: List[Anticipo] = field(default_factory=list)
    descuentos: List[Descuento] = field(default_factory=list)

    detalles: List[Detalle] = field(default_factory=list)

    total_importe: Optional[TotalImporteInvoice] = None
    total_impuestos: Optional[TotalImpuestos] = None

    guias: List[Guia] = field(default_factory=list)
    documentos_relacionados: List[DocumentoRelacionado] = field(default_factory=list)

    observaciones: Optional[str] = None
    orden_de_compra: Optional[str] = None
