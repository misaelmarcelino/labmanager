import os
from typing import Tuple
from app.shared.security.secret_provider import SecretProvider


class EnvSecretProvider(SecretProvider):
    """
    USAR SOMENTE EM DESENVOLVIMENTO LOCAL
    """

    def get_smtp_credentials(self) -> Tuple[str, str]:
        user = os.getenv("SMTP_USER")
        password = os.getenv("SMTP_PASS")

        if not user or not password:
            raise RuntimeError("Credenciais SMTP ausentes no ambiente")

        return user, password
