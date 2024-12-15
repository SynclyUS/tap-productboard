# Productboard Tap

A [Singer](https://www.singer.io) tap for [Productboard](https://www.productboard.com).

## Local Development

Developed with Python 3.13, supports Python 3.9, 3.10, 3.11, 3.12, and 3.13.

You'll need to install [uv](https://github.com/astral-sh/uv).

1. Run `uv sync -p 3.13` to install dependencies.
1. Copy `.env.example` to `.env` and set `TAP_PRODUCTBOARD_API_KEY` to your [Productboard API key](https://syncly.productboard.com/settings/integrations/api-keys)
1. If you want to simulate a partial load of notes, uncomment `TAP_PRODUCTBOARD_START_DATE` in `.env` and set a value of an ISO-601 formatted datetime.

The tap can be run with:

```bash
uv run tap-productboard --config=ENV
```

Or you can run the module directly:

```bash
uv run python -m tap_productboard.tap --config=ENV
```

Tests can be run with pytest:

```bash
uv run pytest
```

### VS Code Launch Configuration

```json
{
    "name": "tap-productboard",
    "type": "debugpy",
    "request": "launch",
    "module": "tap_productboard.tap",
    "args": ["--config", "ENV"],
    "justMyCode": false,
}
```


## Streams

The following streams are currently supported:

- [Companies](https://developer.productboard.com/reference/getcompanies-1)
- [Components](https://developer.productboard.com/reference/getcomponents-1)
- [Features](https://developer.productboard.com/reference/getfeatures-1)
- [Notes](https://developer.productboard.com/reference/getnotes-1)
- [Objectives](https://developer.productboard.com/reference/getobjectives-1)
- [Products](https://developer.productboard.com/reference/getproducts-1)
- [Release Groups](https://developer.productboard.com/reference/listreleasegroups-1)
- [Releases](https://developer.productboard.com/reference/listreleases-1)
- [Users](https://developer.productboard.com/reference/getusers-1)

The following streams are only enabled on some spaces and may be supported in the future:

- [Initiatives](https://developer.productboard.com/reference/getinitiatives)
- [Key Results](https://developer.productboard.com/reference/getkeyresults)

Only the notes stream supports incremental loading. For all others, the full data set is fetched on each run.

### Replication Key

Setting `replication_key` on the stream will trigger incremental loading on endpoints that support filtering on the last updated timestamp. By default the value of `replication_key` will be the same key used to pull the value from the JSON response and used as the query param filter on the request.

Unfortunately, only the notes endpoint supports filtering and uses different keys in the JSON response and the request query param. Adding `replication_param` to a stream where `replication_key` is already set will allow you to override the value used in the request query string param.

```python
>>> from tap_productboard.streams import NotesStream
>>> NotesStream.replication_key
'updatedAt'  # the replication key for the JSON response
>>> NotesStream.replication_param
'updatedFrom'  # the query request string parameter used to filter
```

### Pagination

JSON response objects contain a `$.links.next` key that contains a link to the next page of results. This is true for all endpoints _except_ notes 🙃 which uses a `$.pageCursor` key in the reponse. Why? Who knows. It's all handled for you automatically so just noting here as a WTF.

### API Version

The `X-Version` header is indicated as required for all endpoints, but in practice most seem to operate fine without it. The features endpoint, preferring to be a finicky guy, _does_ require it 🤷🏻‍♂️

The API version can be set per-stream by adding an `api_version` attribute to the class. If not specified, `tap_productboard.client.DEFAULT_API_VERSION` will be used.
