import os
import sys
import functools
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(sys.path)
from MockData import generator as gen

import hashlib

from flask import Flask, request, g

app = Flask(__name__)

table = {}

def cache(key_fun):
    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            key = key_fun(*args, **kwargs)
            if key in table: 
                return table[key]
            value = fun(*args, **kwargs)
            table[key] = value
            return value
        return wrapper
    return decorator

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
