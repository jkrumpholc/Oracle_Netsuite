from base64 import b64encode
from secrets import choice
from string import ascii_letters, digits, punctuation

from nsi_secret_vault.models.secrets import SecretSpec, SecretGenerateRequest, PasswordKey
from nsi_secret_vault.services.secret_store import SecretStore


class PassGenerator:

    def __init__(self, secret_store: SecretStore):
        self.secret_store = secret_store

    async def generate_secret(
        self,
        secret: SecretGenerateRequest,
    ) -> bool:

        spec: SecretSpec = secret.spec
        length: int = spec.length
        if length < 1:
            return False
        symbols: list = spec.symbols.split('-')
        alphabet: str = ""
        if 'alpha' in symbols:
            alphabet += ascii_letters
        if 'num' in symbols:
            alphabet += digits
        if 'symbol' in symbols:
            alphabet += (punctuation + " ")
        password: bytes = ''.join(choice(alphabet) for letter in range(length)).encode('utf-8')
        password_hash = b64encode(password)
        self.secret_store.save(secret.identifier, PasswordKey(
            password_hash=password_hash,
            description=spec.description,
        ))
        return True