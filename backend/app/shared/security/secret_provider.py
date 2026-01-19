from abc import ABC, abstractmethod
from typing import Tuple


class SecretProvider(ABC):
    """
    Contrato para obtenção de segredos sensíveis.
    """

    @abstractmethod
    def get_smtp_credentials(self) -> Tuple[str, str]:
        """Retorna (username, password) do SMTP"""
        pass
