from unittest.mock import MagicMock

from pytest import fixture
from fastapi.testclient import TestClient

from nsi_secret_vault.app import app, ssh_generator_dep, secret_store_dep, pass_generator_dep, gpg_generator_dep
from nsi_secret_vault.services.pass_generator import PassGenerator
from nsi_secret_vault.services.secret_store import SecretStore
from nsi_secret_vault.services.ssh_generator import SSHGenerator


@fixture
def secret_store() -> SecretStore:
    store = SecretStore()
    app.dependency_overrides[secret_store_dep] = lambda: store
    return store

@fixture
def ssh_generator_mock() -> MagicMock:
    mock = MagicMock(spec=SSHGenerator)
    app.dependency_overrides[ssh_generator_dep] = lambda: mock
    return mock

@fixture
def password_generator_mock() -> MagicMock:
    mock = MagicMock(spec=PassGenerator)
    app.dependency_overrides[pass_generator_dep] = lambda: mock
    return mock

@fixture
def gpg_generator_mock() -> MagicMock:
    mock = MagicMock(spec=PassGenerator)
    app.dependency_overrides[gpg_generator_dep] = lambda: mock
    return mock

@fixture
def client(ssh_generator_mock):
    return TestClient(app)