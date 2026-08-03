# local-federated-catalog

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
