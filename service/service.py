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
    g.r = redis.StrictRedis(host=app.config["REDIS_HOST"],
                            port=app.config["REDIS_PORT"],
                            db=app.config["REDIS_DB"])

@app.teardown_request
def _teardown(exception=None):
    del g.r

def cache_wrapper_for(type_name, key_fun, getter, setter):
    def _wrap(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            key = key_fun(*args, **kwargs)
            exists, value = getter(key)
            if exists: return value
            value = fun(*args, **kwargs)
            setter(key, value)
            return value
        return wrapper
    _wrap.__name__ = type_name + "_wrapper"
    return _wrap

def cache_redis(key_fun):
    def redis_set(key, value):
        g.r.set(key, value)
    def redis_lookup(key):
        result = g.r.get(key)
        if result is None: return False, ""
        return True, result
    return cache_wrapper_for("redis", key_fun, redis_lookup, redis_set)

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
        assert len(kwargs.keys()) == 1
        value = list(kwargs.values())[0].lower()
        return key_for(ds, type, value)
    keyfun.__name__ = "_".join((type, keyfun.__name__))
    return cache(keyfun)

@app.route("/dataset/<ds>/given-name/<name>")
@cache_type("given-name")
def given_name(ds, name):
    x = {'given-name' :  gen.gen_first_name()["given_name"]}
    return json.dumps(x)

@app.route("/dataset/<ds>/surname/<name>")
@cache_type("surname")
def surname(ds, name):
    x = {'surname' : gen.gen_last_name()["last_name"]}
    return json.dumps(x)

def _address_keyfun(ds, state, address):
    return key_for(ds, "address", ":".join((state, address)))

def _address1_keyfun(ds, address):
    return key_for(ds, "address", ":".join((address)))

def _full_name_keyfun(ds, full_name):
    return key_for(ds, "full_name", ":".join((full_name)))

def _ssn_keyfun(ds, ssn):
    return key_for(ds, "ssn", ":".join(ssn))

def _bank_keyfun(ds, accountnumber):
    return key_for(ds, "banknumber", ":".join(accountnumber))

def _driver_license_keyfun(ds, licensenumber):
    return key_for(ds, "licensenumber", ":".join(licensenumber))

def _credit_card_keyfun(ds, creditcardnumber):
    return key_for(ds, "creditcardnumber", ":".join(creditcardnumber))

@app.route("/dataset/<ds>/address/<state>/<path:address>")
@cache(_address_keyfun)
def address(ds, state, address):
    if state.upper() not in gen.STATE_CODE_LIST:
        new_state = gen.gen_address('HI')
        new_state['state_code'] = state
        return json.dumps(new_state)
    return json.dumps(gen.gen_address(state))

@app.route("/dataset/<ds>/ssn/<ssn>")
@cache(_ssn_keyfun)
def ssn(ds, ssn):
    new_ssn = {'ssn' : gen.gen_ssn()}
    return json.dumps(new_ssn)

@app.route("/dataset/<ds>/address/<path:address>")
@cache(_address1_keyfun)
def address1(ds, address):
    return json.dumps(gen.gen_address(state=None))

@app.route("/dataset/<ds>/full_name/<path:full_name>")
@cache(_full_name_keyfun)
def full_name(ds, full_name):
    return json.dumps({'name' : gen.gen_full_name()['first_to_last']})

@app.route("/dataset/<ds>/bankaccountnumber/<accountnumber>")
@cache(_bank_keyfun)
def bank_account_number(ds, accountnumber):
    new_account_number = {'bank_account_number' : gen.gen_bank_account()}
    return json.dumps(new_account_number)

@app.route("/dataset/<ds>/driverslicense/<licensenumber>")
@cache(_driver_license_keyfun)
def drivers_license(ds, licensenumber):
    new_license_number = {'drivers_license_number' : gen.gen_drivers_license()}
    return json.dumps(new_license_number)

@app.route("/dataset/<ds>/creditcardnumber/<creditcardnumber>")
@cache(_credit_card_keyfun)
def creditcardnumber(ds, creditcardnumber):
    new_card_number = {'credit_card_number' : gen.gen_credit_card_number()}
    return json.dumps(new_card_number)


if __name__ == "__main__":
    app.debug = True
    app.config.update(
        REDIS_HOST=os.environ.get("REDIS_HOST", "localhost"),
        REDIS_PORT=int(os.environ.get("REDIS_PORT", 6379)),
        REDIS_DB=int(os.environ.get("REDIS_DB", 0))
    )
    app.run(host="0.0.0.0", port=5000)