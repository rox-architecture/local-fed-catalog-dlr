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

Fill-in `"API URL"` and `"API KEY"` with your own values. 

Also, you must provide the `partners.json` file in the repository, which looks like:
```json
{
  "BPNLM67H9AVUVPTD": "did:web:vision-x-api.base-x-ecosystem.org:connectors:dlr-rox-conn",
}
```
This is a list of partners, BPN as the key and the location as the value.

## Funding

This open-source project was developed within the *[ROX](https://www.project-rox.ai/en/)* project. 
This project has received public funding from the **European Union** NextGenerationEU within the Important Project of Common European Interest – Cloud Infrastructures and Services (IPCEI-CIS) under grant agreement 13IPC034.

<p align="center">
  <img alt="Bundesministerium für Wirtschaft und Energie (BMWE)-EU and secunet funding logo" src="bmwe_logo.png" width="400"/>
</p>
