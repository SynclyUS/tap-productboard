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
                    parsed_query = parse_qs(url_parts.query)
                    page_cursor = parsed_query.get("pageCursor", [None])[0]
                    page_offset = parsed_query.get("pageOffset", [None])[0]

                    if page_cursor:
                        params["pageCursor"] = page_cursor
                    elif page_offset:
                        params["pageOffset"] = page_offset

        start_datetime = self.get_starting_timestamp(context)
        if self.replication_key and start_datetime:
            key = getattr(self, "replication_param", self.replication_key)
            params[key] = start_datetime.strftime("%Y-%m-%d")

        return params

    def parse_response(self, response: dict) -> list:
        """
        Process API response to replace 'none' with None in only the timeframe attributes.
        """
        def clean_timeframe(data):
            if isinstance(data, dict) and "timeframe" in data:
                timeframe = data["timeframe"]
                if isinstance(timeframe, dict):
                    for key in ["startDate", "endDate", "granularity"]:
                        if timeframe.get(key) == "none":
                            timeframe[key] = None
            return data

        parsed_data = response.json()
        return [clean_timeframe(record) for record in parsed_data.get("data", [])]
