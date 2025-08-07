from datetime import date
from decimal import Decimal

from xbuilder.domain.entities.invoice import Invoice
from xbuilder.domain.entities.defaults import Defaults
from xbuilder.domain.entities.common import Proveedor, Cliente, Detalle
from xsender.domain.entities.models import Credentials
from xhandler.application.use_cases.handler import Handler

# 1. Create credentials and handler
# Use the beta environment for testing
credentials = Credentials(
    username="MODDATOS",
    password="MODDATOS",
)
handler = Handler(
    wsdl_url="https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService?wsdl",
    credentials=credentials,
)

# 2. Create the invoice and defaults
defaults = Defaults(
    icb_tasa=Decimal("0.50"),
    igv_tasa=Decimal("0.18"),
    ivap_tasa=Decimal("0.04"),
    fecha_emision=date(2023, 10, 12),
)
invoice = Invoice(
    proveedor=Proveedor(
        ruc="20000000001",
        razon_social="EMPRESA SAC",
        nombre_comercial="EMPRESA",
    ),
    cliente=Cliente(
        tipo_documento_identidad="6",
        numero_documento_identidad="20000000002",
        nombre="CLIENTE SAC",
    ),
    serie_numero="F001-1",
    tipo_comprobante="01",
    moneda="PEN",
    detalles=[
        Detalle(
            descripcion="Producto 1",
            cantidad=Decimal("2"),
            precio=Decimal("100"),
            igv_tipo="10",
        ),
        Detalle(
            descripcion="Producto 2",
            cantidad=Decimal("3"),
            precio=Decimal("50"),
            igv_tipo="20",  # Exonerado
        ),
        Detalle(
            descripcion="Bolsa de plastico",
            cantidad=Decimal("10"),
            precio=Decimal("0.1"),
            icb_aplica=True,
        ),
    ],
)

# 3. Define key and cert paths
key_file = "private.key"
cert_file = "public.crt"

# 4. Handle the invoice
print("Processing invoice...")
response = handler.handle(invoice, defaults, key_file, cert_file)

if response.cdr_zip_base64:
    print(f"File sent successfully.")
    # save the cdr to a file
    import base64
    with open("cdr.zip", "wb") as f:
        f.write(base64.b64decode(response.cdr_zip_base64))
    print("CDR saved to cdr.zip")
else:
    print(f"Error sending file: {response.error.code} - {response.error.message}")
    if response.sunat_response:
        print(f"SUNAT Response: {response.sunat_response.status_code} - {response.sunat_response.fault_code} - {response.sunat_response.fault_string}")

if response.xml_zip_base64:
    # save the xml to a file
    import base64
    with open("invoice.zip", "wb") as f:
        f.write(base64.b64decode(response.xml_zip_base64))
    print("XML saved to invoice.zip")
