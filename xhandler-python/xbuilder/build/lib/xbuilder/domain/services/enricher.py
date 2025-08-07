from xbuilder.domain.entities.invoice import Invoice
from xbuilder.domain.entities.defaults import Defaults


class Enricher:
    def enrich(self, invoice: Invoice, defaults: Defaults) -> None:
        self._fill(invoice, defaults)
        self._process(invoice)
        self._summary(invoice)

    def _fill(self, invoice: Invoice, defaults: Defaults) -> None:
        if invoice.moneda is None:
            invoice.moneda = "PEN"

        if invoice.fecha_emision is None:
            invoice.fecha_emision = defaults.date

        if invoice.icb_tasa is None:
            invoice.icb_tasa = defaults.icb_tasa

        if invoice.igv_tasa is None:
            invoice.igv_tasa = defaults.igv_tasa

        if invoice.ivap_tasa is None:
            invoice.ivap_tasa = defaults.ivap_tasa

    def _process(self, invoice: Invoice) -> None:
        for detalle in invoice.detalles:
            if detalle.precio and detalle.igv_tasa:
                detalle.igv = detalle.precio * detalle.igv_tasa

    def _summary(self, invoice: Invoice) -> None:
        from xbuilder.domain.entities.common import TotalImpuestos, TotalImporteInvoice
        from decimal import Decimal

        total_igv = sum(d.igv for d in invoice.detalles if d.igv)
        total_precio = sum(d.precio for d in invoice.detalles if d.precio)

        invoice.total_impuestos = TotalImpuestos(
            total=total_igv,
            ivap_importe=Decimal(0),
            ivap_base_imponible=Decimal(0),
            exportacion_importe=Decimal(0),
            exportacion_base_imponible=Decimal(0),
            gravado_importe=total_igv,
            gravado_base_imponible=total_precio,
            inafecto_importe=Decimal(0),
            inafecto_base_imponible=Decimal(0),
            exonerado_importe=Decimal(0),
            exonerado_base_imponible=Decimal(0),
            gratuito_importe=Decimal(0),
            gratuito_base_imponible=Decimal(0),
            icb_importe=Decimal(0),
            isc_importe=Decimal(0),
            isc_base_imponible=Decimal(0),
        )

        invoice.total_importe = TotalImporteInvoice(
            anticipos=Decimal(0),
            descuentos=Decimal(0),
            importe=total_precio + total_igv,
            importe_sin_impuestos=total_precio,
            importe_con_impuestos=total_precio + total_igv,
        )
