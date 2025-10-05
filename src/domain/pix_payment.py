from datetime import datetime
from enum import Enum

from domain.common.entity import Entity
from domain.common.exception import DomainException
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId


class PaymentStatusEnum(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class PixPayment(Entity):
    def __init__(
        self,
        amount: float,
        provider_payment_id: str,
        pix_payload: str,
        expires_at: datetime,
        status: PaymentStatusEnum = PaymentStatusEnum.PENDING,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined_bulk(
            [
                {"argument": amount, "argument_name": "amount"},
                {
                    "argument": provider_payment_id,
                    "argument_name": "provider_payment_id",
                },
                {"argument": pix_payload, "argument_name": "pix_payload"},
                {"argument": expires_at, "argument_name": "expires_at"},
            ]
        )

        if amount <= 0:
            raise DomainException("amount must be positive")

        super().__init__(id)

        self._amount = amount
        # id returned by payment provider
        self._provider_payment_id = provider_payment_id
        # pix_payload / qr_code: string to show to the user or to decode
        self._pix_payload = pix_payload
        # ISO8601 timestamp or provider-specific expiry
        self._expires_at = expires_at
        self._status = status

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def status(self) -> PaymentStatusEnum:
        return self._status

    @property
    def provider_payment_id(self) -> str:
        return self._provider_payment_id

    @property
    def pix_payload(self) -> str:
        return self._pix_payload

    @property
    def expires_at(self) -> datetime:
        return self._expires_at
