from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Defaults:
    icb_tasa: Decimal
    igv_tasa: Decimal
    ivap_tasa: Decimal
    date: date
