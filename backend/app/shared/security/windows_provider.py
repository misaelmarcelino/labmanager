import win32cred
from typing import Tuple
from app.shared.security.secret_provider import SecretProvider


class WindowsSecretProvider(SecretProvider):
    def __init__(self, credential_name: str):
        self.credential_name = credential_name

    def get_smtp_credentials(self) -> Tuple[str, str]:
        cred = win32cred.CredRead(
            self.credential_name,
            win32cred.CRED_TYPE_GENERIC,
            0
        )

        username = cred["UserName"]
        password = cred["CredentialBlob"].decode("utf-16")

        return username, password
