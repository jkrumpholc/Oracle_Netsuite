from typing import Any, Optional

from nsi_secret_vault.models.secrets import SSHKey, PasswordKey, GPGKey


class SecretStore:
    """
    Hey, I'm a very secure encrypted store!
    Trust me.
    """
    storage: dict[str, Any] = {}

    def save(self, identifier: str, secret: Any):
        self.storage[identifier] = secret

    def get(self, identifier: str) -> SSHKey | PasswordKey | GPGKey | None:
        return self.storage.get(identifier)
