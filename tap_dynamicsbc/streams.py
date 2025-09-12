"""Stream type classes for tap-dynamicsbc."""

from __future__ import annotations

import typing as t

from singer_sdk import SchemaDirectory, StreamSchema
from tap_dynamicsbc.client import DynamicsBusinessCentralStream
from tap_dynamicsbc import schemas


SCHEMAS_DIR = SchemaDirectory(schemas)


class ClientsStream(DynamicsBusinessCentralStream):
    name = "clients"
    path = "/apiCustomerCards"
    primary_keys: t.ClassVar[list[str]] = ["no"]
    replication_key = "lastModifiedDateTime"
    schema = StreamSchema(SCHEMAS_DIR)

    def get_url_params(
        self,
        context: t.Any | None = None,  # noqa: ARG002
        next_page_token: t.Any | None = None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        params = super().get_url_params(context, next_page_token)
        if params.get("$filter"):
            params["$filter"] += " and "
        else:
            params["$filter"] = ""
        params["$filter"] += "eCommerce eq false"
        return params


class ProductsStream(DynamicsBusinessCentralStream):
    name = "products"
    path = "/ItemCard"
    primary_keys: t.ClassVar[list[str]] = ["No"]
    replication_key = "Last_Date_Modified"
    schema = StreamSchema(SCHEMAS_DIR)


class PricesStream(DynamicsBusinessCentralStream):
    name = "prices"
    path = "/itemprice"
    primary_keys: t.ClassVar[list[str]] = ["Price_List_Code", "Line_No"]
    schema = StreamSchema(SCHEMAS_DIR)
    
    def get_url_params(
        self,
        context: t.Any | None = None,  # noqa: ARG002
        next_page_token: t.Any | None = None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        params = super().get_url_params(context, next_page_token)
        params["$filter"] = "Price_List_Code eq '01'"
        return params


class UnitsStream(DynamicsBusinessCentralStream):
    name = "units"
    path = "/ItemUnits"
    primary_keys: t.ClassVar[list[str]] = ["Code"]
    schema = StreamSchema(SCHEMAS_DIR)


class SellerStream(DynamicsBusinessCentralStream):
    name = "sellers"
    path = "/Vendedor_Card"
    primary_keys: t.ClassVar[list[str]] = ["Code"]
    schema = StreamSchema(SCHEMAS_DIR)