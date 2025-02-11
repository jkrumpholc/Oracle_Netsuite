from asyncio import create_subprocess_exec
from pathlib import Path
from tempfile import TemporaryDirectory

from nsi_secret_vault.models.secrets import SecretSpec, SecretGenerateRequest, SSHKey
from nsi_secret_vault.services.secret_store import SecretStore


class SSHGenerator:

    def __init__(self, secret_store: SecretStore):
        self.secret_store = secret_store

    async def generate_secret(
        self,
        secret: SecretGenerateRequest,
    ) -> bool:

        spec: SecretSpec = secret.spec

        with TemporaryDirectory() as temp_dir:
            file_loc = Path(temp_dir) / 'ssh_key'
            args = [
                '-t', spec.ssh_key_type,
                '-N', spec.passphrase,
                '-C', spec.description,
                '-b', str(spec.bits),
                '-f', file_loc
            ]
            proc = await create_subprocess_exec(
                'ssh-keygen',
                *args
            )
            await proc.wait()

            if proc.returncode != 0:
                return False

            with open(file_loc, 'rb') as f:
                ssh_key = f.read()

        self.secret_store.save(secret.identifier, SSHKey(
            key_type=spec.key_type,
            description=spec.description,
            contents=ssh_key,
        ))
        return True
