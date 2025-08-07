from dataclasses import dataclass
from typing import Optional


@dataclass
class Credentials:
    username: str
    password: str


@dataclass
class ErrorResponse:
    code: str
    message: str


@dataclass
class SendFileResponse:
    cdr: Optional[str] = None
    ticket: Optional[str] = None
    error: Optional[ErrorResponse] = None


@dataclass
class VerifyTicketStatus:
    cdr_base64: str
    status_code: str


@dataclass
class VerifyTicketResponse:
    status: Optional[VerifyTicketStatus] = None
    error: Optional[ErrorResponse] = None
