from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Response, status

from nsi_secret_vault.models.secrets import (
    SecretGenerateRequest, SecretGetResponse,
)
from nsi_secret_vault.services.secret_store import SecretStore
from nsi_secret_vault.services.ssh_generator import SSHGenerator
from nsi_secret_vault.services.pass_generator import PassGenerator
from nsi_secret_vault.services.gpg_generator import GPGGenerator

app = FastAPI()


def secret_store_dep() -> SecretStore:
    return SecretStore()


def ssh_generator_dep(
        secret_store: Annotated[SecretStore, Depends(secret_store_dep)]
) -> SSHGenerator:
    return SSHGenerator(secret_store)


def pass_generator_dep(
        secret_store: Annotated[SecretStore, Depends(secret_store_dep)]
) -> PassGenerator:
    return PassGenerator(secret_store)


def gpg_generator_dep(
        secret_store: Annotated[SecretStore, Depends(secret_store_dep)]
) -> GPGGenerator:
    return GPGGenerator(secret_store)


@app.get("/secret")
async def get_secret(
        identifier: str,
        secret_store: Annotated[SecretStore, Depends(secret_store_dep)]
) -> SecretGetResponse:
    secret = secret_store.get(identifier)
    if secret is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return SecretGetResponse(identifier=identifier, secret=secret)


@app.post("/secret")
async def create_secret(
        secret: SecretGenerateRequest,
        ssh_generator: Annotated[SSHGenerator, Depends(ssh_generator_dep)],
        pass_generator: Annotated[PassGenerator, Depends(pass_generator_dep)],
        gpg_generator: Annotated[GPGGenerator, Depends(gpg_generator_dep)],
):
    match secret.secret_type:
        case "SSH":
            ret = await ssh_generator.generate_secret(secret)
        case "PASS":
            ret = await pass_generator.generate_secret(secret)
        case "GPG":
            ret = await gpg_generator.generate_secret(secret)
        case _:
            ret = False
    if ret:
        return Response(status_code=status.HTTP_201_CREATED)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/health")
def health_check() -> Response:
    return Response(status_code=status.HTTP_200_OK)
