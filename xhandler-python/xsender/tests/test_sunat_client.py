import pytest
from unittest.mock import MagicMock, patch

from xsender.domain.entities.models import Credentials
from xsender.infrastructure.implementation.sunat_client import SunatClient


@pytest.fixture
def mock_zeep_client():
    with patch("xsender.infrastructure.implementation.sunat_client.Client") as mock:
        yield mock


def test_send_file_success_ticket(mock_zeep_client):
    # Arrange
    mock_service = MagicMock()
    mock_service.sendBill.return_value = MagicMock(ticket="test_ticket")
    mock_zeep_client.return_value.service = mock_service

    credentials = Credentials(username="testuser", password="testpassword")
    client = SunatClient(wsdl_url="http://example.com?wsdl", credentials=credentials)

    # Act
    response = client.send_file("test.xml", b"<xml></xml>")

    # Assert
    assert response.ticket == "test_ticket"
    assert response.cdr is None
    assert response.error is None


def test_send_file_success_cdr(mock_zeep_client):
    # Arrange
    mock_service = MagicMock()
    mock_service.sendBill.return_value = MagicMock(content="test_cdr")
    delattr(mock_service.sendBill.return_value, 'ticket') # ensure ticket is not present
    mock_zeep_client.return_value.service = mock_service

    credentials = Credentials(username="testuser", password="testpassword")
    client = SunatClient(wsdl_url="http://example.com?wsdl", credentials=credentials)

    # Act
    response = client.send_file("test.xml", b"<xml></xml>")

    # Assert
    assert response.cdr == "test_cdr"
    assert response.ticket is None
    assert response.error is None


def test_send_file_error(mock_zeep_client):
    # Arrange
    mock_service = MagicMock()
    mock_service.sendBill.side_effect = Exception("SOAP Error")
    mock_zeep_client.return_value.service = mock_service

    credentials = Credentials(username="testuser", password="testpassword")
    client = SunatClient(wsdl_url="http://example.com?wsdl", credentials=credentials)

    # Act
    response = client.send_file("test.xml", b"<xml></xml>")

    # Assert
    assert response.error is not None
    assert response.error.code == "client_error"
    assert response.error.message == "SOAP Error"


def test_verify_ticket_success(mock_zeep_client):
    # Arrange
    mock_service = MagicMock()
    mock_service.getStatus.return_value = MagicMock(
        content="test_cdr_base64", statusCode="0"
    )
    mock_zeep_client.return_value.service = mock_service

    credentials = Credentials(username="testuser", password="testpassword")
    client = SunatClient(wsdl_url="http://example.com?wsdl", credentials=credentials)

    # Act
    response = client.verify_ticket("test_ticket")

    # Assert
    assert response.status is not None
    assert response.status.cdr_base64 == "test_cdr_base64"
    assert response.status.status_code == "0"
    assert response.error is None


def test_verify_ticket_error(mock_zeep_client):
    # Arrange
    mock_service = MagicMock()
    mock_service.getStatus.side_effect = Exception("SOAP Error")
    mock_zeep_client.return_value.service = mock_service

    credentials = Credentials(username="testuser", password="testpassword")
    client = SunatClient(wsdl_url="http://example.com?wsdl", credentials=credentials)

    # Act
    response = client.verify_ticket("test_ticket")

    # Assert
    assert response.error is not None
    assert response.error.code == "client_error"
    assert response.error.message == "SOAP Error"
