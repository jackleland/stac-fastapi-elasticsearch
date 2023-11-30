"""API configuration."""
import os
from typing import Any, Dict, Set

from elasticsearch import AsyncElasticsearch, Elasticsearch  # type: ignore
from stac_fastapi.types.config import ApiSettings



def _es_config() -> Dict[str, Any]:
    config = {
        "hosts": [
            f'{os.getenv("ES_HOST")}:{os.getenv("ES_PORT")}/'
        ],
        "headers": {
            # "accept": "application/vnd.elasticsearch+json; compatible-with=7"
            "x-api-key": os.getenv("ES_API_KEY"),
        },
        "timeout": 900,
        "use_ssl": False,
        "verify_certs": False,
        "ssl_show_warn": False,
    }

    if (u := os.getenv("ES_USER")) and (p := os.getenv("ES_PASS")):
        config["http_auth"] = (u, p)

    if (v := os.getenv("ES_USE_SSL")) and v == "true":
        config["use_ssl"] = True

    if (v := os.getenv("ES_VERIFY_CERTS")) and v == "true":
        config["verify_certs"] = True

    if (v := os.getenv("ES_SSL_SHOW_WARN")) and v == "true":
        config["ssl_show_warn"] = True

    if v := os.getenv("CURL_CA_BUNDLE"):
        config["ca_certs"] = v

    return config


_forbidden_fields: Set[str] = {"type"}


class ElasticsearchSettings(ApiSettings):
    """API settings."""

    # Fields which are defined by STAC but not included in the database model
    forbidden_fields: Set[str] = _forbidden_fields
    indexed_fields: Set[str] = {"properties"}

    @property
    def create_client(self):
        """Create es client."""
        return Elasticsearch(**_es_config())


class AsyncElasticsearchSettings(ApiSettings):
    """API settings."""

    # Fields which are defined by STAC but not included in the database model
    forbidden_fields: Set[str] = _forbidden_fields
    indexed_fields: Set[str] = {"properties"}

    @property
    def create_client(self):
        """Create async elasticsearch client."""
        return AsyncElasticsearch(**_es_config())
