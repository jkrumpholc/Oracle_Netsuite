from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from nsi_secret_vault.models.secrets import SecretGenerateRequest, SSHKey
from nsi_secret_vault.services.secret_store import SecretStore


def test_secret_not_found(client: TestClient):
    response = client.get("/secret?identifier=gator")
    assert response.status_code == 404


def test_ssh_secret_generated(
    client: TestClient,
    ssh_generator_mock: MagicMock,
    secret_store: SecretStore,
):
    identifier = 'gator'

    def generate_secret(
        secret: SecretGenerateRequest
    ) -> bool:
        secret_store.save(
            identifier,
            SSHKey(
                key_type='ed25519',
                description="isn't it nice here",
                contents=b'by the lagoon'
            )
        )
        return True

    ssh_generator_mock.generate_secret.side_effect = generate_secret

    response = client.post(
        "/secret",
        json={
            'identifier': identifier,
            'spec': {
                'description': "isn't it nice here",
                'key_type': 'ed25519',
                'passphrase': "it's never too late to take in the view",
                'bits': 256
            }
        }
    )
    assert response.status_code == 201

    response = client.get(
        f"/secret?identifier={identifier}",
    )
    assert response.status_code == 200
    assert response.json() == {
        'identifier': 'gator',
        'secret': {
            'contents': 'by the lagoon',
            'description': "isn't it nice here",
            'key_type': 'ed25519'
        }
    }


def test_ssh_secret_failed_to_generate(
    client: TestClient,
    ssh_generator_mock: MagicMock,
    secret_store: SecretStore,
):
    identifier = 'gator'

    def generate_secret(
        secret: SecretGenerateRequest
    ) -> bool:
        return False

    ssh_generator_mock.generate_secret.side_effect = generate_secret

    response = client.post(
        "/secret",
        json={
            'identifier': identifier,
            'spec': {
                'description': "isn't it nice here",
                'key_type': 'ed25519',
                'passphrase': "it's never too late to take in the view",
                'bits': 256
            }
        }
    )
    assert response.status_code == 500
