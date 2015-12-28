# Lookup Service

## Running

First install redis, and make sure `redis-server` is in your path.

### Setup the Service

```bash
mkdir .virtualenv
virtualenv .virtualenv
source .virtualenv/bin/activate
pip3 install -r requirements.txt
```

### Run the Service

```bash
source .virtualenv/bin/activate
python3 service.py
```

To run with custom redis options use:

```bash
source .virtualenv/bin/activate
env REDIS_HOST=<host> REDIS_PORT=<port> REDIS_DB=<db> python3 service.py
```

## API

### `GET /dataset/<dataset>/given-name/<given name>`

Yields a new given name for the given given name. Names will be consistent within
a dataset. `/dataset/1/given-name/Bob` will yield the same name on subsequent
calls, but `/dataset/2/given-name/Bob` may return a different name. The dataset
parameter can be any arbitrary text exuding the forward-slash character. The
`<given name>` field is normalized to lowercase so `Bob` and `bob` are considered
one name. However, misspellings are not handled so `Bob` and `Bov` are not considered
the same name.

### `GET /dataset/<dataset>/last-name/<last name>`

Follows the same rules as the `given-name` endpoint, but for last names.

### `GET /dataset/<dataset>/address/<state>/address/<address>`

Returns a new random address for the given address. Like with the name endpoints,
calls using the same dataset parameter will return the same address if the `<state>`
and `<address>` parameters match. The `<state>` parameter specifies the state the
generated address is located in as a two-letter, upper-case state code like "AZ".
