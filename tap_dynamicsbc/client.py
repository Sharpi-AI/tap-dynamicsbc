"""REST client handling, including DynamicsBusinessCentralStream base class."""

from __future__ import annotations

import decimal
import typing as t
from functools import cached_property
from importlib import resources

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BaseOffsetPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

from tap_dynamicsbc.auth import DynamicsBusinessCentralAuthenticator

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Auth, Context


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"


class DynamicsBusinessCentralPaginator(BaseOffsetPaginator):
    """Paginator for Dynamics Business Central OData API."""

    def __init__(self, start_value: int = 0, page_size: int = 1000) -> None:
        """Initialize the paginator.
        
        Args:
            start_value: The starting offset value.
            page_size: The number of records per page.
        """
        super().__init__(start_value, page_size)
        self.page_size = page_size

    def get_next(self, response: requests.Response) -> t.Any | None:
        """Get the next page token from the response.
        
        Args:
            response: The HTTP response object.
            
        Returns:
            The next offset value, or None if no more pages.
        """
        data = response.json()
        
        # Check for OData nextLink
        if "@odata.nextLink" in data:
            return self.current_value + self.page_size
            
        # Check if we got a full page of results
        records = data.get("value", [])
        if len(records) < self.page_size:
            return None
            
        return self.current_value + self.page_size


class DynamicsBusinessCentralStream(RESTStream):
    """DynamicsBusinessCentral stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$[*]"

    # Update this value if necessary or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def url_base(self) -> str:
        return self.config["base_url"]

    @cached_property
    def authenticator(self) -> Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return DynamicsBusinessCentralAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {}

    def get_new_paginator(self) -> BaseAPIPaginator | None:
        """Create a new pagination helper instance.

        Returns:
            A pagination helper instance for Dynamics Business Central OData API.
        """
        return DynamicsBusinessCentralPaginator(start_value=0, page_size=1000)

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value (offset).

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        
        # Add OData pagination parameters
        paginator = self.get_new_paginator()
        if paginator:
            params["$top"] = paginator.page_size
            if next_page_token:
                params["$skip"] = next_page_token
        
        # Add ordering for replication key if present
        if self.replication_key:
            params["$orderby"] = f"{self.replication_key} asc"
            
        return params

    def prepare_request_payload(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ARG002, ANN401
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )

    def post_process(
        self,
        row: dict,
        context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Note: As of SDK v0.47.0, this method is automatically executed for all stream types.
        You should not need to call this method directly in custom `get_records` implementations.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row
