from typing import Literal

from pydantic import BaseModel


class SecretSpec(BaseModel):
    key_type: Literal['dsa', 'ecdsa', 'ecdsa-sk', 'ed25519', 'ed25519-sk', 'rsa']  # -t
    passphrase: str  # - N
    description: str  # -C
    bits: int  # -b


class SSHKey(BaseModel):
    key_type: Literal['dsa', 'ecdsa', 'ecdsa-sk', 'ed25519', 'ed25519-sk', 'rsa']
    description: str
    contents: bytes


class Secret(BaseModel):
    spec: SecretSpec


class SecretGenerateRequest(BaseModel):
    identifier: str
    spec: SecretSpec


class SecretGetResponse(BaseModel):
    identifier: str
    secret: SSHKey
