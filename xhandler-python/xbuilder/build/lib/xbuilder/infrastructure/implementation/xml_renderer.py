import os
from decimal import Decimal
from jinja2 import Environment, FileSystemLoader

from xbuilder.domain.entities.invoice import Invoice
from xbuilder.domain.entities.common import TipoFormaDePago


def multiply100(value: Decimal) -> Decimal:
    return value * 100


def round_decimal(value: Decimal) -> str:
    if value is None:
        return ""
    return f"{value:.2f}"


def format03d(value: int) -> str:
    return f"{value:03d}"


def is_credito(value: TipoFormaDePago) -> bool:
    return value == TipoFormaDePago.CREDITO


def is_gt0(value: Decimal) -> bool:
    return value > Decimal(0)


class XmlRenderer:
    def __init__(self):
        template_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "templates"
        )
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.filters["multiply100"] = multiply100
        self.env.filters["round_decimal"] = round_decimal
        self.env.filters["format03d"] = format03d
        self.env.tests["credito"] = is_credito
        self.env.tests["gt0"] = is_gt0

    def render_invoice(self, invoice: Invoice) -> str:
        template = self.env.get_template("renderer/invoice.xml")
        return template.render(invoice.__dict__)
