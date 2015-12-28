import random 
from pprint import pprint

def _id(x): return x

def _rpick(index, array, lookup=_id):
    low = 0
    high = len(array) - 1
    while True:
        if high == low:
            return high
        elif high - low == 1 and (index >= lookup(array[low]) 
                             and index <= lookup(array[high])):
            return high
        pivot = (low + high) // 2
        value = lookup(array[pivot])
        if index < value:
            high = pivot
        elif index > value:
            low = pivot
        else:
            return pivot

class StateWeightedRandom(object):
    def __init__(self, state_dict):
        self.rates = []
        total = sum(state_dict.values())
        print(total)
        next_rate = 0.0
        for code, rate in state_dict.items():
            next_rate += float(rate) / total
            self.rates.append((code, next_rate))
        pprint(self.rates)
        print(len(self.rates))

    def next(self): # -> State Code
        index = random.random()
        # print("picked:", index)
        rate_index = _rpick(index, self.rates,
                            lookup=lambda v: v[1])
        return self.rates[rate_index][0]

if __name__ == "__main__":
    foo = {'AK': 127,
     'AL': 8969,
     'AR': 5354,
     'AZ': 2106,
     'CA': 12101,
     'CO': 2336,
     'CT': 332,
     'DC': 596,
     'DE': 85,
     'FL': 17271,
     'GA': 6617,
     'HI': 60,
     'IA': 2616,
     'ID': 168,
     'IL': 6890,
     'IN': 5325,
     'KS': 2401,
     'KY': 3377,
     'LA': 3892,
     'MA': 555,
     'MD': 715,
     'ME': 138,
     'MI': 10954,
     'MN': 3147,
     'MO': 4456,
     'MS': 2903,
     'MT': 138,
     'NC': 7854,
     'ND': 117,
     'NE': 1474,
     'NH': 141,
     'NJ': 1041,
     'NM': 236,
     'NV': 341,
     'NY': 1907,
     'OH': 8068,
     'OK': 3569,
     'OR': 2009,
     'PA': 8168,
     'PR': 244,
     'RI': 85,
     'SC': 4123,
     'SD': 686,
     'TN': 10263,
     'TX': 25223,
     'UT': 265,
     'VA': 5616,
     'VT': 60,
     'WA': 3340,
     'WI': 3128,
     'WV': 1576,
     'WY': 90}

    bar = {'CA' : 39144818,
    'TX' : 27469114,
    'FL' : 20271272,
    'NY' : 19795791,
    'IL' : 12859995,
    'PA' : 12802503,
    'OH' : 11613423,
    'GA' : 10214860,
    'NC' : 10042802,
    'MI' : 9922576,
    'NJ' : 8958013,
    'VA' : 8382993,
    'WA' : 7170351,
    'AZ' : 6828065,
    'MA' : 6794422,
    'IN' : 6619680,
    'TN' : 6600299,
    'MO' : 6083672,
    'MD' : 6006401,
    'WI' : 5771337,
    'MN' : 5489594,
    'CO' : 5456574,
    'SC' : 4896146,
    'AL' : 4858979,
    'LA' : 4670724,
    'KY' : 4425092,
    'OR' : 4028977,
    'OK' : 3911338,
    'CT' : 3590886,
    'PR' : 3474182,
    'IA' : 3123899,
    'UT' : 2995919,
    'MS' : 2992333,
    'AR' : 2978204,
    'KS' : 2911641,
    'NV' : 2890845,
    'NM' : 2085109,
    'NE' : 1896190,
    'WV' : 1844128,
    'ID' : 1654930,
    'HI' : 1431603,
    'NH' : 1330608,
    'ME' : 1329328,
    'RI' : 1056298,
    'MT' : 1032949,
    'DE' : 945934,
    'SD' : 858469,
    'ND' : 756927,
    'AK' : 738432,
    'DC' : 672228,
    'VT' : 626042,
    'WY' : 586107,}

    baz = {'UT' : 4, 'WY' : 3, 'CA' : 93}

    def count_names(data_list, data_value):
        if data_value in data_list:
            try:
                data_list[data_value] += 1
            except:
                # print(data_list)
                print(data_value)
                raise
        else:
            data_list[data_value] = 1
        return data_list

    ####  foo/bar/baz
    test_set = baz

    t = StateWeightedRandom(test_set)
    counter = {}

    for x in range(193253):
        count_names(counter, t.next())


    from pprint import pprint

    for k, v in counter.items():
        ####  foo/bar/baz
        print("\t".join((k, str(v), str(test_set[k]), str(v - test_set[k]))))


    ####  foo/bar/baz
    print(len(counter), len(test_set))
