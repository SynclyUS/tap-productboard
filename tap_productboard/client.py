import json
from functools import cached_property
from pathlib import Path
from typing import Any, Optional, Union
from urllib.parse import parse_qs, urlparse

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.exceptions import FatalAPIError
from singer_sdk.helpers.types import Auth, Context
from singer_sdk.streams import RESTStream

DEFAULT_API_VERSION = "1"


class ProductboardStream(RESTStream):
    """Base Productboard stream class."""

    url_base = "https://api.productboard.com"

    primary_keys = ["id"]

    next_page_token_jsonpath = "$.links.next"
    records_jsonpath = "$.data[*]"

    @property
    def authenticator(self) -> Auth:
        """If api_key is in config, return a BearerTokenAuthenticator."""
        api_key = self.config.get("api_key")
        if api_key:
            return BearerTokenAuthenticator(self, api_key)
        raise FatalAPIError("No valid authentication method found")

    @property
    def http_headers(self) -> dict:
        """
        Set the required X-Version header for the Productboard API version.
        Optionally set custom User-Agent or Productboard-Partner-Id headers.
        """
        headers = {"X-Version": getattr(self, "api_version", DEFAULT_API_VERSION)}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        if "partner_id" in self.config:
            headers["Productboard-Partner-Id"] = self.config.get("partner_id")
        return headers

    @cached_property
    def schema(self) -> dict:
        """Load schema from the schemas directory based on the stream name."""
        path = Path(__file__).parent / "schemas" / f"{self.name}.json"
        return json.loads(path.read_text())

    def get_url_params(
        self, context: Optional[Context], next_page_token: Optional[Any]
    ) -> Union[dict[str, Any], str]:
        """Set the pagination param and the replication param, if applicable."""

        params = {}

        if next_page_token:
            if next_page_token.startswith("https"):
                url_parts = urlparse(next_page_token)
                if url_parts.query:
                    o = parse_qs(url_parts.query)
                    next_page_token = o.get("pageCursor")
            params["pageCursor"] = next_page_token

        start_datetime = self.get_starting_timestamp(context)
        if self.replication_key and start_datetime:
            key = getattr(self, "replication_param", self.replication_key)
            params[key] = start_datetime.strftime("%Y-%m-%d")

        return params
