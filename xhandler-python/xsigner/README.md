# xsigner

A Python library to sign UBL XML files using `xmlsec`.

## Installation

Install the package with `uv`:

```bash
uv pip install -e .
```

This library depends on the `xmlsec1` binary being installed on your system. Please see the [xmlsec documentation](https://xmlsec.readthedocs.io/en/stable/install.html) for installation instructions.

## Usage

```python
from xsigner.domain.services.signer import Signer

# 1. Create a signer
signer = Signer()

# 2. Get the XML content, private key, and certificate
with open("path/to/your.xml", "r") as f:
    xml_content = f.read()

with open("path/to/your.key", "r") as f:
    key_file = f.read()

with open("path/to/your.crt", "r") as f:
    cert_file = f.read()

# 3. Sign the XML
signed_xml = signer.sign(xml_content, key_file, cert_file)

print(signed_xml)
```
