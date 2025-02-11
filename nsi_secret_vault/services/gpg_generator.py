from gnupg import GPG
from tempfile import TemporaryDirectory
from pathlib import Path

from nsi_secret_vault.models.secrets import SecretSpec, SecretGenerateRequest, GPGKey
from nsi_secret_vault.services.secret_store import SecretStore


class GPGGenerator:

    def __init__(self, secret_store: SecretStore):
        self.secret_store = secret_store

    async def generate_secret(
        self,
        secret: SecretGenerateRequest,
    ) -> bool:

        spec: SecretSpec = secret.spec
        length: int = spec.gpg_key_length
        key_type: str = spec.gpg_key_type
        with TemporaryDirectory() as temp_dir:
            file_loc = Path(temp_dir) / 'gpg_key'

            gpg = GPG(str(file_loc))
            content = gpg.gen_key_input(key_type=key_type, key_length=length)
            self.secret_store.save(secret.identifier, GPGKey(
                content=content,
                description=spec.description,
            ))
        return True
