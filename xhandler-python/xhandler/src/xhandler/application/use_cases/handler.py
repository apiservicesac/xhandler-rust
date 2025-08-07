from xbuilder.domain.entities.invoice import Invoice
from xbuilder.domain.entities.defaults import Defaults
from xbuilder.domain.services.enricher import Enricher
from xbuilder.infrastructure.implementation.xml_renderer import XmlRenderer

from xsigner.domain.services.signer import Signer

from xsender.domain.entities.models import Credentials
from xsender.infrastructure.implementation.sunat_client import SunatClient


class Handler:
    def __init__(self, wsdl_url: str, credentials: Credentials):
        self.enricher = Enricher()
        self.renderer = XmlRenderer()
        self.signer = Signer()
        self.sender = SunatClient(wsdl_url, credentials)

    def handle(
        self,
        invoice: Invoice,
        defaults: Defaults,
        key_file: str,
        cert_file: str,
    ):
        # 1. Enrich
        self.enricher.enrich(invoice, defaults)

        # 2. Render
        xml_to_sign = self.renderer.render_invoice(invoice)

        # 3. Sign
        signed_xml = self.signer.sign(xml_to_sign, key_file, cert_file)

        # 4. Send
        filename = f"{invoice.proveedor.ruc}-{invoice.tipo_comprobante}-{invoice.serie_numero}.xml"
        response = self.sender.send_file(filename, signed_xml.encode("utf-8"))

        return response
