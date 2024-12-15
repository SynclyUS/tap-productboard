from typing import Sequence

from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from tap_productboard.streams import (
    CompaniesStream,
    ComponentsStream,
    FeaturesStream,
    NotesStream,
    ObjectivesStream,
    ProductsStream,
    ReleaseGroupsStream,
    ReleasesStream,
    UsersStream,
)

STREAMS = [
    CompaniesStream,
    UsersStream,
    ProductsStream,
    NotesStream,
    FeaturesStream,
    ComponentsStream,
    ObjectivesStream,
    ReleaseGroupsStream,
    ReleasesStream,
]


class TapProductboard(Tap):
    """Singer tap for Productboard."""

    name = "tap-productboard"

    config_jsonschema = th.PropertiesList(
        th.Property("api_key", th.StringType, required=True, title="API Key"),
        th.Property(
            "partner_id", th.StringType, required=False, title="Productboard Partner ID"
        ),
        th.Property("start_date", th.DateTimeType, required=False, title="Start Date"),
        th.Property(
            "user_agent", th.StringType, required=False, title="Custom User Agent"
        ),
    ).to_dict()

    def discover_streams(self) -> Sequence[Stream]:
        """Return a list of discovered streams."""
        discovered_streams = []
        for stream_class in STREAMS:
            try:
                stream = stream_class(tap=self)
                discovered_streams.append(stream)
            # pylint: disable-next=broad-exception-caught
            except Exception as e:
                self.logger.error("Error discovering stream %s: %s", stream_class, e)
        return discovered_streams


if __name__ == "__main__":
    # pylint: disable-next=no-value-for-parameter
    TapProductboard.cli()
