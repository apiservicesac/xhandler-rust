from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional, List


@dataclass
class Contacto:
    telefono: str
    email: str


@dataclass
class Direccion:
    ubigeo: Optional[str] = None
    codigo_local: Optional[str] = None
    urbanizacion: Optional[str] = None
    departamento: Optional[str] = None
    provincia: Optional[str] = None
    distrito: Optional[str] = None
    direccion: Optional[str] = None
    codigo_pais: Optional[str] = None


@dataclass
class Proveedor:
    ruc: str
    razon_social: str
    nombre_comercial: Optional[str] = None
    direccion: Optional[Direccion] = None
    contacto: Optional[Contacto] = None


@dataclass
class Firmante:
    ruc: str
    razon_social: str


@dataclass
class Cliente:
    tipo_documento_identidad: str
    numero_documento_identidad: str
    nombre: str
    direccion: Optional[Direccion] = None
    contacto: Optional[Contacto] = None


@dataclass
class Detraccion:
    medio_de_pago: str
    cuenta_bancaria: str
    tipo_bien_detraido: str
    porcentaje: Decimal
    monto: Optional[Decimal] = None


class TipoFormaDePago(Enum):
    CREDITO = "Credito"
    CONTADO = "Contado"


@dataclass
class CuotaDePago:
    importe: Decimal
    fecha_pago: date


@dataclass
class FormaDePago:
    tipo: Optional[TipoFormaDePago] = None
    cuotas: List[CuotaDePago] = field(default_factory=list)
    total: Optional[Decimal] = None


@dataclass
class Percepcion:
    tipo: str
    porcentaje: Optional[Decimal] = None
    monto: Optional[Decimal] = None
    monto_base: Optional[Decimal] = None
    monto_total: Optional[Decimal] = None


@dataclass
class Anticipo:
    tipo: Optional[str] = None
    comprobante_serie_numero: str = ""
    comprobante_tipo: Optional[str] = None
    monto: Decimal = Decimal(0)


@dataclass
class Descuento:
    tipo: Optional[str] = None
    monto: Decimal = Decimal(0)
    monto_base: Optional[Decimal] = None
    factor: Optional[Decimal] = None


@dataclass
class Guia:
    tipo_documento: str
    serie_numero: str


@dataclass
class DocumentoRelacionado:
    tipo_documento: str
    serie_numero: str


@dataclass
class Detalle:
    descripcion: str
    cantidad: Decimal
    unidad_medida: Optional[str] = None
    precio: Optional[Decimal] = None
    precio_con_impuestos: Optional[Decimal] = None
    precio_referencia: Optional[Decimal] = None
    precio_referencia_tipo: Optional[str] = None
    igv_tasa: Optional[Decimal] = None
    icb_tasa: Optional[Decimal] = None
    isc_tasa: Optional[Decimal] = None
    igv_tipo: Optional[str] = None
    isc_tipo: Optional[str] = None
    icb_aplica: bool = False
    icb: Optional[Decimal] = None
    igv: Optional[Decimal] = None
    igv_base_imponible: Optional[Decimal] = None
    isc: Optional[Decimal] = None
    isc_base_imponible: Optional[Decimal] = None
    total_impuestos: Optional[Decimal] = None


@dataclass
class TotalImporteInvoice:
    anticipos: Decimal
    descuentos: Decimal
    importe: Decimal
    importe_sin_impuestos: Decimal
    importe_con_impuestos: Decimal


@dataclass
class TotalImporteNote:
    importe: Decimal
    importe_sin_impuestos: Decimal


@dataclass
class TotalImpuestos:
    total: Decimal
    ivap_importe: Decimal
    ivap_base_imponible: Decimal
    exportacion_importe: Decimal
    exportacion_base_imponible: Decimal
    gravado_importe: Decimal
    gravado_base_imponible: Decimal
    inafecto_importe: Decimal
    inafecto_base_imponible: Decimal
    exonerado_importe: Decimal
    exonerado_base_imponible: Decimal
    gratuito_importe: Decimal
    gratuito_base_imponible: Decimal
    icb_importe: Decimal
    isc_importe: Decimal
    isc_base_imponible: Decimal
