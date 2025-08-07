from datetime import date
from decimal import Decimal

from xbuilder.domain.entities.defaults import Defaults
from xbuilder.domain.entities.invoice import Invoice
from xbuilder.domain.entities.common import Proveedor, Cliente
from xbuilder.domain.services.enricher import Enricher


def test_enricher_fill():
    # Arrange
    defaults = Defaults(
        icb_tasa=Decimal("0.2"),
        igv_tasa=Decimal("0.18"),
        ivap_tasa=Decimal("0.04"),
        date=date(2023, 1, 1),
    )
    invoice = Invoice(
        proveedor=Proveedor(ruc="12345678912", razon_social="My Company"),
        cliente=Cliente(
            tipo_documento_identidad="6",
            numero_documento_identidad="12121212121",
            nombre="Customer",
        ),
    )
    enricher = Enricher()

    # Act
    enricher.enrich(invoice, defaults)

    # Assert
    assert invoice.moneda == "PEN"
    assert invoice.fecha_emision == date(2023, 1, 1)
    assert invoice.icb_tasa == Decimal("0.2")
    assert invoice.igv_tasa == Decimal("0.18")
    assert invoice.ivap_tasa == Decimal("0.04")
