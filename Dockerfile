FROM container-registry-frankfurt.oracle.com/os/oraclelinux:9-slim as build

RUN microdnf install python3.12 python3.12-pip
RUN python3.12 -m venv --copies /tmp/app/venv
RUN python3.12 -m pip install poetry  poetry-plugin-export

ADD . /tmp/build/
WORKDIR /tmp/build/

RUN poetry export --format=requirements.txt --output /tmp/build/requirements.txt \
    && /tmp/app/venv/bin/pip3 install -r /tmp/build/requirements.txt

RUN poetry build --format wheel && \
    /tmp/app/venv/bin/pip3 install --find-links /tmp/build/dist/ nsi_secret_vault

FROM container-registry-frankfurt.oracle.com/os/oraclelinux:9-slim as app

RUN microdnf install python3.12 openssh

COPY --from=build /tmp/app /app

EXPOSE 8000
CMD ["/app/venv/bin/python3", "-m", "uvicorn", "nsi_secret_vault.app:app", "--host", "127.0.0.1", "--port", "8000"]
