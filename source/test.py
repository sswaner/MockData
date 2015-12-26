from config import source_path
from pprint import pprint
import json

f = open(source_path + 'address.json')
foo = json.load(f)
# pprint(foo)
f.close()
import random

stateCodeList = stateNamexRef = ['MS', 'IA', 'OK',
    'WY', 'MN', 'IL', 'AR',
    'NM', 'IN', 'MD', 'LA',
    'TX', 'AZ', 'WI', 'MI',
    'KS', 'UT', 'VA', 'OR',
    'CT', 'MT', 'CA', 'MA',
    'WV', 'DE', 'NH', 'VT',
    'GA', 'ND', 'HI', 'PA',
    'FL', 'AK', 'KY',
    'TN', 'SC', 'NE', 'MO',
    'OH', 'AL', 'RI', 'SD',
    'CO', 'ID', 'NJ', 'WA',
    'NC', 'NY',
    'NV', 'ME']



def test1():
	scx = random.randrange(0, len(stateCodeList) -1)
	state_code = stateCodeList[scx]

	state_list = [x for x in foo if x['state_code'] == state_code]
	x = random.randrange(0, len(state_list) -1)
	print (state_list[x])



for i in range(300000):
	test1()