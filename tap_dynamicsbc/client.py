"""REST client handling, including DynamicsBusinessCentralStream base class."""

from __future__ import annotations

import decimal
import backoff
import requests
import typing as t
from functools import cached_property
from importlib import resources
from singer_sdk.exceptions import RetriableAPIError, FatalAPIError

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

    def __init__(self, start_value: int = 0, page_size: int = 5000) -> None:
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

    records_jsonpath = "$.value[*]"

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
    def backoff_max_tries(self) -> int:
        return 3

    def request_decorator(self, func: t.Callable) -> t.Callable:
        decorator: t.Callable = backoff.on_exception(
            backoff.expo,
            (
                RetriableAPIError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.RequestException,
                ConnectionError,
            ),
            max_tries=5,
            factor=2,
        )(func)
        return decorator

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
        return DynamicsBusinessCentralPaginator(start_value=0, page_size=5000)

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
        
        paginator = self.get_new_paginator()
        if paginator:
            params["$top"] = paginator.page_size
            if next_page_token:
                params["$skip"] = next_page_token
        
        if self.replication_key and context is not None:
            params["$filter"] = f"{self.replication_key} gt {context.get('replication_key')}"
            
        return params

    def _request(
        self,
        prepared_request: requests.PreparedRequest,
        context: dict | None,  # noqa: ANN401, ARG002
    ) -> requests.Response:
        """Execute a prepared request and handle authentication errors.
        
        Args:
            prepared_request: The prepared request to execute.
            context: The stream context.
            
        Returns:
            The HTTP response.
            
        Raises:
            FatalAPIError: If authentication fails after retry.
        """
        response = super()._request(prepared_request, context)
        
        # Handle 401 Unauthorized errors by refreshing the token and retrying once
        if response.status_code == 401:
            self.logger.info("Received 401 Unauthorized, refreshing access token")
            self.authenticator.refresh_access_token()
            
            # Re-authenticate and retry the request once
            prepared_request = self.authenticator(prepared_request)
            response = super()._request(prepared_request, context)
            
            # If still getting 401, raise a fatal error
            if response.status_code == 401:
                raise FatalAPIError("Authentication failed after token refresh")
                
        return response

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )
