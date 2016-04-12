# from config import source_path
# from pprint import pprint
# import json
# import time
import MockData.generator as gen

# t1 = time.time()
# f = open(source_path + 'address.json')
# foo = json.load(f)
# # pprint(foo)
# f.close()
# t2 = time.time()

# deserialize_time = t2 - t1
# state_addresses = {}
# t1 = time.time()
# sa = open(source_path + 'state-address.json')
# state_addresses = json.load(sa)
# t2 = time.time()
# deserialize_time = t2 - t1

# import random

# stateCodeList = stateNamexRef = ['MS', 'IA', 'OK',
#     'WY', 'MN', 'IL', 'AR',
#     'NM', 'IN', 'MD', 'LA',
#     'TX', 'AZ', 'WI', 'MI',
#     'KS', 'UT', 'VA', 'OR',
#     'CT', 'MT', 'CA', 'MA',
#     'WV', 'DE', 'NH', 'VT',
#     'GA', 'ND', 'HI', 'PA',
#     'FL', 'AK', 'KY',
#     'TN', 'SC', 'NE', 'MO',
#     'OH', 'AL', 'RI', 'SD',
#     'CO', 'ID', 'NJ', 'WA',
#     'NC', 'NY', 
#     'NV', 'ME', 'DC']



# def test1():
# 	scx = random.randrange(0, len(stateCodeList) -1)
# 	state_code = stateCodeList[scx]

# 	state_list = [x for x in foo if x['state_code'] == state_code]
# 	x = random.randrange(0, len(state_list) -1)
# 	# print (state_list[x])

# def test2():
#     scx = random.randrange(0, len(stateCodeList) -1)
#     state_code = stateCodeList[scx]
#     try:
#         x = random.randrange(0, len(state_addresses[state_code]) -1)
#     except:
#         print(state_code)
#         raise
#     return state_addresses[state_code][x]

# def test3():
#     for state in stateCodeList:
#         print(state, len(state_addresses[state]))

# def reload_and_parse():
#     for state in stateCodeList:
#         state_addresses[state] = []


#     for address in foo:
#         if address['state_code'] in stateCodeList:
#             state_addresses[address['state_code']].append(address)

#     f = open(source_path + 'state-addresses.json', 'w+')
#     json.dump(state_addresses, f)
#     f.close()
# # t1 = time.time()
# # for i in range(1000):
# # 	test1()
# # t2 = time.time()
# # print('test1: ', str(t2-t1))
# # print('-' * 80)

# t1 = time.time()
# # for i in range(1000):
# test3()
# t2 = time.time()
# print('test3: ', str(t2-t1))
# # print('time: ', str(t2-t1))
# print('deserialize_time: ', deserialize_time)