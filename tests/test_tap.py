import datetime

from singer_sdk.testing import get_tap_test_class

from tap_productboard.tap import TapProductboard

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
}


# Run standard built-in tap tests from the SDK:
TestTapExample = get_tap_test_class(tap_class=TapProductboard, config=SAMPLE_CONFIG)
