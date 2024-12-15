import json
from functools import cached_property
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.exceptions import FatalAPIError
from singer_sdk.helpers.types import Auth, Context
from singer_sdk.streams import RESTStream
from singer_sdk.streams.rest import _TToken

DEFAULT_API_VERSION = "1"


class ProductboardStream(RESTStream):

    next_page_token_jsonpath = "$.links.next"
    records_jsonpath = "$.data[*]"
    url_base = "https://api.productboard.com"

    @property
    def authenticator(self) -> Auth:
        api_key = self.config.get("api_key")
        if api_key:
            return BearerTokenAuthenticator(self, api_key)
        raise FatalAPIError("No valid authentication method found")

    @property
    def http_headers(self) -> dict:
        headers = {"X-Version": getattr(self, "api_version", DEFAULT_API_VERSION)}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        if "partner_id" in self.config:
            headers["Productboard-Partner-Id"] = self.config.get("partner_id")
        return headers

    @cached_property
    def schema(self) -> dict:
        path = Path(__file__).parent / "schemas" / f"{self.name}.json"
        return json.loads(path.read_text())

    def get_url_params(
        self, context: Context, next_page_token: _TToken
    ) -> dict[str, Any] | str:

        params = {}

        if next_page_token:
            if next_page_token.startswith("https"):
                url_parts = urlparse(next_page_token)
                if url_parts.query:
                    params = parse_qs(url_parts.query)
                    next_page_token = params.get("pageCursor")
            params["pageCursor"] = next_page_token

        start_datetime = self.get_starting_timestamp(context)
        if self.replication_key and start_datetime:
            key = getattr(self, "replication_param", self.replication_key)
            params[key] = start_datetime.strftime("%Y-%m-%d")

        return params
