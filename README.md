# local-federated-catalog

## Run without a container

Install with

```bash
uv sync
```
Run with

```bash
export CONNECTOR_MANAGEMENT_API=<insert-value>
export CONNECTOR_API_KEY=<insert-value>
export PARTNER_MAPPING_PATH=<insert-value>
uvicorn local_fc.main:app
```

## Container build

```bash
docker build -t local-federated-catalog:0.1.0 .
```

To run
```bash
docker run --rm \
  --name local-federated-catalog \
  -p 8000:8000 \
  -e CONNECTOR_MANAGEMENT_API="API URL" \
  -e CONNECTOR_API_KEY="API KEY" \
  -e PARTNER_MAPPING_PATH="/app/config/partner-mapping.json" \
  -v "$(pwd)/partners.json:/app/config/partner-mapping.json:ro" \
  local-federated-catalog:0.1.0
```

## Pre-built images registry

https://github.com/rox-architecture/local-fed-catalog-dlr/pkgs/container/local-federated-catalog-dlr
