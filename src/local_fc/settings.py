from pydantic import Field, HttpUrl
from pydantic.alias_generators import to_camel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings read from environment variables."""

    model_config = SettingsConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    catalog_fetcher_timeout_seconds: int = Field(
        20,
        title="Catalog Fetcher Timeout Seconds",
        description="Timeout of the catalog fetcher HTTP client.",
        examples=[20],
    )

    connector_api_key: str = Field(
        title="Connector API Key",
        description="The API for the connector.",
        examples=["sk-4tvn340z0n3v094zn03vz30"],
    )

    connector_management_api: HttpUrl = Field(
        title="Connector Management API",
        description="The management API endpoint of the connector.",
        examples=["https://www.example.com/management/"],
    )

    did_resolver_timeout_seconds: int = Field(
        10,
        title="DID Resolver Timeout Seconds",
        description="Timeout of the DID Resolver HTTP client.",
        examples=[10],
    )

    dsp_service_id: str = Field(
        "dsp-url",
        title="DSP Service ID",
        description="ID of the DSP service in the DID document.",
        examples=["dsp-url"],
    )

    federated_collector_concurreny_max: int = Field(
        10,
        title="Federated Collector Concurrency Max",
        description="Maximum concurrent fetchers for the federated collection.",
        examples=[10],
    )

    federated_collector_poll_interval_seconds: float = Field(
        60.0,
        title="Federated Collector Poll Interval Seconds",
        description="Interval for the federated collection.",
        examples=[60.0],
    )

    federated_collector_retries_delay_seconds: int = Field(
        3,
        title="Federated Collector Retries Delay Seconds",
        description="Delay between retries for the collection of a single catalog.",
        examples=[3],
    )

    federated_collector_retries_max: int = Field(
        3,
        title="Federated Collector Retries Max",
        description="Maximal number of retries for the collection of a single catalog.",
        examples=[3],
    )
