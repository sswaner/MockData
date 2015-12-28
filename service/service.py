import os
import sys
import functools
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from MockData import generator as gen
import redis
import hashlib
from flask import Flask, request, g
import json

app = Flask(__name__)

table = {}

@app.before_request
def _before():
    g.r = redis.StrictRedis(host=app.config.get("REDIS_HOST", "localhost"),
                            port=app.config.get("REDIS_PORT", 6379),
                            db=app.config.get("REDIS_DB", 0))

@app.teardown_request
def _teardown(exception=None):
    g.r.close()

def cache_wrapper_for(type_name, key_fun, getter, setter):
    def _wrap(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            key = key_fun(*args, **kwargs)
            exists, value = lookup(key)
            if exists: return value
            value = fun(*args, **kwargs)
            setter(key, value)
            return value
    _wrap.__name__ = type_name + "_wrapper"
    return _wrap

def cache_redis(key_fun):
    def redis_lookup(key):
        result = g.r.get(key)
        if result is None: return False, ""
        return True, result
    return cache_wrapper_for("redis", key_fun, redis_lookup, g.r.set)

def cache_debug(key_fun):
    table = {}
    def debug_lookup(key):
        if key not in table: return False, ""
        return True, table[key]
    def debug_setter(key, value):
        table[key] = value
    return cache_wrapper_for("debug", key_fun, debug_lookup, debug_setter)

def cache(key_fun):
    return cache_redis(key_fun)

def key_for(dataset, type, value):
    key_str = (":".join((dataset, type, value)))
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

def cache_type(type):
    def keyfun(ds, **kwargs):
        print(kwargs.keys())
        assert len(kwargs.keys()) == 1
        value = list(kwargs.values())[0].lower()
        return key_for(ds, type, value)
    keyfun.__name__ = "_".join((type, keyfun.__name__))
    return cache(keyfun)

@app.route("/dataset/<ds>/given-name/<name>")
@cache_type("given-name")
def given_name(ds, name):
    return gen.gen_first_name()["given_name"]

@app.route("/dataset/<ds>/surname/<name>")
@cache_type("surname")
def surname(ds, name):
    return gen.gen_last_name()["last_name"]

def _address_keyfun(ds, state, address):
    return key_for(ds, "address", ":".join((state, address)))

@app.route("/dataset/<ds>/address/<state>/<path:address>")
@cache(_address_keyfun)
def address(ds, state, address):
    return gen.gen_address(state)

if __name__ == "__main__":
    app.debug = True
    app.run()
