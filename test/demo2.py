import os
import sys
import functools
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import urllib
import requests
from MockData import generator as gen
import json
from tabulate import tabulate

base_url = 'http://127.0.0.1:5000'

table = []
for i in range(100):
    a = gen.gen_last_name()['last_name']
    # print(a)
    a_quote = urllib.parse.quote("|".join(a))
    b = requests.get("{1}/dataset/foo/surname/{0}".format(a_quote, base_url))
    # print(b.text)
    # print(json.loads(b.text))
    # print("|".join(a.values()) + "\t ----------> \t", "|".join(json.loads(b.text).values()))
    table.append([a, ' >>> ', b.text])
print(tabulate(table))