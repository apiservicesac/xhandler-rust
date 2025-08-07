# xbuilder

A Python library to build UBL XML files for Peruvian standards.

## Installation

Install the package with `uv`:

```bash
uv pip install -e .
```

## Usage

```python
from datetime import date
from decimal import Decimal

from xbuilder.domain.entities.invoice import Invoice
from xbuilder.domain.entities.defaults import Defaults
from xbuilder.domain.entities.common import Proveedor, Cliente
from xbuilder.domain.services.enricher import Enricher
from xbuilder.infrastructure.implementation.xml_renderer import XmlRenderer

# 1. Create the invoice object
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

# 2. Create the defaults and enricher
defaults = Defaults(
    icb_tasa=Decimal("0.2"),
    igv_tasa=Decimal("0.18"),
    ivap_tasa=Decimal("0.04"),
    date=date(2023, 1, 1),
)
enricher = Enricher()
enricher.enrich(invoice, defaults)

# 3. Create the renderer and render the XML
renderer = XmlRenderer()
xml_content = renderer.render_invoice(invoice)

print(xml_content)
```

## Architecture

This module follows the Hexagonal Architecture (Clean Architecture).
- **Domain**: Contains the core business logic and entities.
- **Application**: Contains the use cases that orchestrate the domain logic.
- **Infrastructure**: Contains the implementation details, such as frameworks, databases, and external services.
```
