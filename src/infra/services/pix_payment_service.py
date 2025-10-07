from datetime import datetime, timedelta
from uuid import uuid4

from application.services.ipix_payment_service import IPixPaymentService
from domain.pix_payment import PaymentStatusEnum, PixPayment


class PixPaymentService(IPixPaymentService):
    async def create_payment(self, amount: float) -> PixPayment:
        """
        Creates a new PIX payment with the specified amount.
        In a real implementation, this would integrate with a payment provider.
        """
        # Generate mock payment data - in real implementation, this would call external API
        provider_payment_id = f"pix_{uuid4().hex[:12]}"

        # Generate a mock PIX payload (in real scenario, this comes from payment provider)
        pix_payload = f"00020126580014br.gov.bcb.pix013636{provider_payment_id}5204000053039865802BR5925MINDHUB SERVICOS MEDICOS6009SAO PAULO62070503***6304{self._calculate_crc(provider_payment_id)}"

        # Set expiration to 30 minutes from now
        expires_at = datetime.now() + timedelta(minutes=30)

        return PixPayment(
            amount=amount,
            provider_payment_id=provider_payment_id,
            pix_payload=pix_payload,
            expires_at=expires_at,
            status=PaymentStatusEnum.PENDING,
        )

    def _calculate_crc(self, provider_id: str) -> str:
        """Mock CRC calculation for PIX payload"""
        # In real implementation, this would calculate proper CRC16
        return str(abs(hash(provider_id)) % 10000).zfill(4)
