import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from decimal import Decimal

from xbuilder.domain.entities.invoice import Invoice
from xbuilder.domain.entities.defaults import Defaults
from xbuilder.domain.entities.common import Proveedor, Cliente
from xsender.domain.entities.models import Credentials, SendFileResponse
from xhandler.application.use_cases.handler import Handler


@pytest.fixture
def mock_sunat_client():
    with patch("xhandler.application.use_cases.handler.SunatClient") as mock:
        yield mock


def test_handler_success(mock_sunat_client):
    # Arrange
    mock_sender_instance = mock_sunat_client.return_value
    mock_sender_instance.send_file.return_value = SendFileResponse(ticket="test_ticket")

    credentials = Credentials(username="testuser", password="testpassword")
    handler = Handler(wsdl_url="http://example.com?wsdl", credentials=credentials)

    # We need to manually set the sender mock on the handler instance
    handler.sender = mock_sender_instance

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
    key_file = os.path.join(os.path.dirname(__file__), "private.key")
    cert_file = os.path.join(os.path.dirname(__file__), "public.crt")

    # Act
    response = handler.handle(invoice, defaults, key_file, cert_file)

    # Assert
    assert response.ticket == "test_ticket"
    mock_sender_instance.send_file.assert_called_once()
