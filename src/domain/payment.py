from enum import Enum

from domain.common.entity import Entity
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId


class PaymentMethodEnum(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PIX = "pix"
    CASH = "cash"


class Payment(Entity):
    def __init__(
        self,
        amount: float,
        method: PaymentMethodEnum,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined_bulk(
            [
                {"argument": amount, "argument_name": "amount"},
                {"argument": method, "argument_name": "method"},
            ]
        )

        super().__init__(id)
        self.amount = amount
        self.method = method
