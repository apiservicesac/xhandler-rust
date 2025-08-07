# xsender

A Python library to send UBL XML files to SUNAT.

## Installation

Install the package with `uv`:

```bash
uv pip install -e .
```

## Usage

```python
from xsender.domain.entities.models import Credentials
from xsender.infrastructure.implementation.sunat_client import SunatClient

# 1. Create credentials and client
credentials = Credentials(username="your_username", password="your_password")
client = SunatClient(
    wsdl_url="https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService?wsdl",
    credentials=credentials,
)

# 2. Get the file content
with open("path/to/your.xml", "rb") as f:
    content = f.read()

# 3. Send the file
response = client.send_file("your_file.xml", content)

if response.ticket:
    print(f"File sent successfully. Ticket: {response.ticket}")
elif response.cdr:
    print(f"File sent successfully. CDR: {response.cdr}")
else:
    print(f"Error sending file: {response.error.code} - {response.error.message}")

```
