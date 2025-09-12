"""DynamicsBusinessCentral tap class."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from decimal import Decimal

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_dynamicsbc import streams


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Decimal and datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class TapDynamicsBusinessCentral(Tap):
    """DynamicsBusinessCentral tap class."""
    name = "tap-dynamicsbc"

    def write_message(self, message) -> None:
        """Write a message to stdout with ensure_ascii=False."""
        json.dump(message.to_dict(), sys.stdout, ensure_ascii=False, separators=(",", ":"), cls=DecimalEncoder)
        sys.stdout.write("\n")
        sys.stdout.flush()
        
    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Client ID",
            description="The client ID to authenticate against the API service",
        ),
        th.Property(
            "client_secret",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Client Secret",
            description="The client secret to authenticate against the API service",
        ),
        th.Property(
            "auth_url",
            th.StringType(nullable=False),
            required=True,
            title="Auth URL",
            description="The auth URL to authenticate against the API service",
        ),
        th.Property(
            "base_url",
            th.StringType(nullable=False),
            required=True,
            title="API URL",
            description="The API URL to authenticate against the API service",
        ),
        th.Property(
            "oauth_scopes",
            th.StringType(nullable=False),
            required=True,
            title="OAuth Scopes",
            description="The OAuth scopes to authenticate against the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.DynamicsBusinessCentralStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.ProductsStream(self),
            streams.PricesStream(self),
            streams.UnitsStream(self),
            streams.SellerStream(self),
            streams.ClientsStream(self),
        ]


if __name__ == "__main__":
    TapDynamicsBusinessCentral.cli()
