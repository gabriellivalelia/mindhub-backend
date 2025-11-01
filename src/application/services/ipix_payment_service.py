from abc import ABC, abstractmethod

from domain.pix_payment import PixPayment


class IPixPaymentService(ABC):
    @abstractmethod
    async def create_payment(self, amount: float) -> PixPayment:
        """Cria um novo pagamento PIX com o valor especificado"""
        pass
