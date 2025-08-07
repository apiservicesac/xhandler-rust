# xhandler

A Python library that orchestrates the xbuilder, xsigner, and xsender modules to provide a complete solution for generating, signing, and sending UBL XML files to SUNAT.

## Installation

Install the package with `uv`:

```bash
uv pip install -e .
```

This will also install the local `xbuilder`, `xsigner`, and `xsender` modules.

## Usage

```python
from datetime import date
from decimal import Decimal

from xbuilder.domain.entities.invoice import Invoice
from xbuilder.domain.entities.defaults import Defaults
from xbuilder.domain.entities.common import Proveedor, Cliente
from xsender.domain.entities.models import Credentials
from xhandler.application.use_cases.handler import Handler

# 1. Create credentials and handler
credentials = Credentials(username="your_username", password="your_password")
handler = Handler(
    wsdl_url="https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService?wsdl",
    credentials=credentials,
)

# 2. Create the invoice and defaults
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
    serie_numero="F001-1",
    tipo_comprobante="01"
)

# 3. Define key and cert paths
key_file = "path/to/your.key"
cert_file = "path/to/your.crt"

# 4. Handle the invoice
response = handler.handle(invoice, defaults, key_file, cert_file)

if response.ticket:
    print(f"File sent successfully. Ticket: {response.ticket}")
elif response.cdr:
    print(f"File sent successfully. CDR: {response.cdr}")
else:
    print(f"Error sending file: {response.error.code} - {response.error.message}")
```
