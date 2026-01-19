import platform
from app.core.config import get_settings
from app.shared.security.windows_provider import WindowsSecretProvider
from app.shared.security.env_provider import EnvSecretProvider
from app.shared.security.secret_provider import SecretProvider

settings = get_settings()
def get_secret_provider() -> SecretProvider:
    """
    Resolve o provider correto conforme ambiente.
    """

    if platform.system() == "Windows" and settings.SMTP_CREDENTIAL_NAME:
        return WindowsSecretProvider(settings.SMTP_CREDENTIAL_NAME)

    return EnvSecretProvider()
