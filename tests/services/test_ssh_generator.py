from asyncio.subprocess import Process
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest import fixture

from nsi_secret_vault.models.secrets import SecretGenerateRequest, SecretSpec, SSHKey
from nsi_secret_vault.services import ssh_generator
from nsi_secret_vault.services.secret_store import SecretStore
from nsi_secret_vault.services.ssh_generator import SSHGenerator


class TestSshGenerator:

    fs: FakeFilesystem
    mock_subprocess_create: MagicMock

    secret_store: SecretStore
    generator: SSHGenerator

    _request = SecretGenerateRequest(
        identifier='croc',
        spec=SecretSpec(
            key_type='ed25519',
            description="isn't it nice here",
            passphrase="it's never too late to take in the view",
            bits=256,
        )
    )

    @fixture(autouse=True)
    def setup(self, fs: FakeFilesystem):
        self.fs = fs
        self.secret_store = SecretStore()
        self.generator = SSHGenerator(secret_store=self.secret_store)

        with patch.object(ssh_generator, 'create_subprocess_exec') as sp_create:
            self.mock_subprocess_create = sp_create
            yield

    @pytest.mark.asyncio
    async def test_successful_generate(self):
        proccess = MagicMock(spec=Process)
        proccess.returncode = 0

        def create_subprocess(*args):
            with open(Path(args[-1]), "w") as fh:
                fh.write('by the lagoon')
            return proccess

        self.mock_subprocess_create.side_effect = create_subprocess
        assert await self.generator.generate_secret(self._request)

        secret = self.secret_store.get('croc')
        assert secret is not None
        assert secret == SSHKey(
            key_type='ed25519',
            description="isn't it nice here",
            contents=b'by the lagoon'
        )

    @pytest.mark.asyncio
    async def test_failed_generate(self):
        self.mock_subprocess_create.return_value.returncode = 1
        assert not await self.generator.generate_secret(self._request)