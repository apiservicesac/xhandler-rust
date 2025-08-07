import base64
import zipfile
from io import BytesIO
from typing import Optional

from zeep import Client, Settings, Transport
from zeep.wsse.username import UsernameToken

from xsender.domain.entities.models import (
    Credentials,
    SendFileResponse,
    VerifyTicketResponse,
    ErrorResponse,
    VerifyTicketStatus,
)


class SunatClient:
    def __init__(self, wsdl_url: str, credentials: Credentials):
        self.credentials = credentials
        self.client = Client(wsdl_url, wsse=UsernameToken(credentials.username, credentials.password))

    def send_file(self, filename: str, content: bytes) -> SendFileResponse:
        # Zip the content
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(filename, content)
        zip_content = zip_buffer.getvalue()

        # Base64 encode the zip
        encoded_zip = base64.b64encode(zip_content).decode("utf-8")

        try:
            response = self.client.service.sendBill(fileName=filename, contentFile=encoded_zip)
            if hasattr(response, "ticket"):
                return SendFileResponse(ticket=response.ticket)
            elif hasattr(response, "content"):
                return SendFileResponse(cdr=response.content)
            else:
                return SendFileResponse(error=ErrorResponse(code="unknown", message="Unknown response"))
        except Exception as e:
            return SendFileResponse(error=ErrorResponse(code="client_error", message=str(e)))

    def verify_ticket(self, ticket: str) -> VerifyTicketResponse:
        try:
            response = self.client.service.getStatus(ticket=ticket)
            if hasattr(response, "statusCode"):
                return VerifyTicketResponse(
                    status=VerifyTicketStatus(
                        cdr_base64=response.content,
                        status_code=response.statusCode,
                    )
                )
            else:
                return VerifyTicketResponse(error=ErrorResponse(code="unknown", message="Unknown response"))
        except Exception as e:
            return VerifyTicketResponse(error=ErrorResponse(code="client_error", message=str(e)))
