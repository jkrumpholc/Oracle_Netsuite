from typing import Literal, Optional

from pydantic import BaseModel


class SecretSpec(BaseModel):
    # Common
    description: Optional[str]  # -C

    # SSH
    ssh_key_type: Literal['dsa', 'ecdsa', 'ecdsa-sk', 'ed25519', 'ed25519-sk', 'rsa'] = None  # -t
    passphrase: str = None  # - N
    bits: int = None  # -b

    # Password
    length: int = None  # -l
    symbol_group: Literal['alpha', 'num', 'alpha-num', 'alpha-num-symbol'] = None  # -g


class SSHKey(BaseModel):
    key_type: Literal['dsa', 'ecdsa', 'ecdsa-sk', 'ed25519', 'ed25519-sk', 'rsa']
    description: Optional[str] # -C
    contents: bytes


class PasswordKey(BaseModel):
    description: Optional[str]  # -C
    password_hash: bytes


class SecretGenerateRequest(BaseModel):
    identifier: str
    secret_type: Literal['SSH', 'PASS']
    spec: SecretSpec


class SecretGetResponse(BaseModel):
    identifier: str
    secret: SSHKey | PasswordKey
