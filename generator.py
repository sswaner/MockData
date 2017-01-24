"""Mock Data Generator"""
import sys
import os
import random
import json
import pickle
import datetime
import string
import math
import bisect

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from MockData.names_list import last_names, female_names, male_names
from MockData.names_list import male_name_tuples, female_name_tuples
from MockData.names_list import last_name_tuples

import MockData.config as config

from MockData.config import data_path
from MockData.data import word_lists

# last_name_tuples.sort(key=lambda r: r[0])

LAST_NAME_KEYS = [r[0] for r in last_name_tuples]
MALE_NAME_KEYS = [r[0] for r in male_name_tuples]
FEMALE_NAME_KEYS = [r[0] for r in female_name_tuples]

GENDER_BIAS = 53
# LAST_NAME = {'last_name' : None, 'case' : None}
# FIRST_NAME = {'given_name' : None, 'case' : None, 'gender' : None, 'ordinal' : 0}
# FULL_NAME = {'first_to_last' : None, 'last_then_first' : None,
#              'gender' : None,
#              'given_names' : [], 'surname' : None}


stateNamexRef = {'Mississippi': 'MS', 'Iowa': 'IA', 'Oklahoma': 'OK',
                 'Wyoming': 'WY', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR',
                 'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA',
                 'Texas': 'TX', 'Arizona': 'AZ', 'Wisconsin': 'WI', 'Michigan': 'MI',
                 'Kansas': 'KS', 'Utah': 'UT', 'Virginia': 'VA', 'Oregon': 'OR',
                 'Connecticut': 'CT', 'Montana': 'MT', 'California': 'CA', 'Massachusetts': 'MA',
                 'West Virginia': 'WV', 'Delaware': 'DE', 'New Hampshire': 'NH', 'Vermont': 'VT',
                 'Georgia': 'GA', 'North Dakota': 'ND', 'Hawaii': 'HI', 'Pennsylvania': 'PA',
                 'Puerto Rico': 'PR', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY',
                 'Tennessee': 'TN', 'South Carolina': 'SC', 'Nebraska': 'NE', 'Missouri': 'MO',
                 'Ohio': 'OH', 'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD',
                 'Colorado': 'CO', 'Idaho': 'ID', 'New Jersey': 'NJ', 'Washington': 'WA',
                 'North Carolina': 'NC', 'New York': 'NY', 'District of Columbia': 'DC',
                 'Nevada': 'NV', 'Maine': 'ME'}

STATE_CODE_LIST = [
    'MS', 'IA', 'OK', 'WY',
    'MN', 'IL', 'AR', 'NM',
    'IN', 'MD', 'LA', 'TX',
    'AZ', 'WI', 'MI', 'KS',
    'UT', 'VA', 'OR', 'CT',
    'MT', 'CA', 'MA', 'WV',
    'DE', 'NH', 'VT', 'GA',
    'ND', 'HI', 'PA', 'FL',
    'AK', 'KY', 'TN', 'SC',
    'NE', 'MO', 'OH', 'AL',
    'RI', 'SD', 'CO', 'ID',
    'NJ', 'WA', 'NC', 'NY',
    'NV', 'ME'
]

address_data = open(data_path + 'state-address.json')
STATE_ADDRESS_LIST = json.load(address_data)


def gen_last_name(ucase=2, lcase=2,
                  compound_name=False, use_census_distribution=True):
    gen_name = {}

    ln = None
    cn = None
    if use_census_distribution:
        x = random.randrange(1, 905441)
        ln = last_name_tuples[bisect.bisect(LAST_NAME_KEYS, x)][1]


    if compound_name == True:
        xc = random.randrange(0, 905441)
        cn = last_name_tuples[bisect.bisect(LAST_NAME_KEYS, xc)][1]

        ln = ln + '-' + cn

    u = random.randrange(0, 100)
    if u < ucase:
        gen_name['last_name'] = ln
        gen_name['case'] = 'u'
    elif u > 100 - lcase:
        gen_name['last_name'] = ln.swapcase()
        gen_name['case'] = 'l'
    else:
        gen_name['last_name'] = ln.title()
        gen_name['case'] = 'p'
    gen_name['seed'] = x
    return gen_name

def gen_last_name_v1(ucase=2, lcase=2,
                  compound_name=False, use_census_distribution=True):
    gen_name = {}

    ln = None
    cn = None
    if use_census_distribution:
        while ln is None:
            x = random.randrange(0, 905540)
            for (k, v) in last_names:
                if x > k:
                    ln = v
    else:
        while ln is None:
            x = random.randrange(len(last_names))
            ln = last_names[x][1]


    if compound_name == True:
        xc = random.randrange(0, 905540)
        # print(x)
        while cn is None:
            # try:
            #     cn = last_names[x]
            # except:
            #     x = x + 1
            #     pass
            if xc in last_names:
                cn = last_names[x]
            else:
                xc += 1
        ln = ln + '-' + cn
    u = random.randrange(0, 100)
    if u < ucase:
        gen_name['last_name'] = ln
        gen_name['case'] = 'u'
    elif u > 100 - lcase:
        gen_name['last_name'] = ln.swapcase()
        gen_name['case'] = 'l'
    else:
        gen_name['last_name'] = ln.title()
        gen_name['case'] = 'p'
    gen_name['seed'] = x
    x = None
    return gen_name

def gen_first_name(ucase=2, lcase=2, gender=False):
    """Generate a random first name."""
    gen_name = {}
    
    if not gender:
        if random.randrange(1,100) > GENDER_BIAS:
            gender = 'f'
        else:
            gender = 'm'

    _name = None
    _male_name_seed = random.randrange(1, 90040)
    _female_name_seed = random.randrange(1500, 90024) #1500?  Too many Patricia's
    
    if gender == 'f':
        _name = female_name_tuples[bisect.bisect(FEMALE_NAME_KEYS, _female_name_seed)][1]
    else:
        _name = male_name_tuples[bisect.bisect(MALE_NAME_KEYS, _male_name_seed)][1]


    _random = random.randrange(0, 100)
    if _random < ucase:
        gen_name['given_name'] = _name
        gen_name['case'] = 'u'
    elif _random > 100 - lcase:
        gen_name['given_name'] = _name.swapcase()
        gen_name['case'] = 'l'
    else:
        gen_name['given_name'] = _name.title()
        gen_name['case'] = 'p'
    gen_name['gender'] = gender

    return gen_name

def gen_first_name_v1(ucase=2, lcase=2, gender=False):
    """Generate a random first name."""
    gen_name = {}
    _last_name = None
    _male_name_seed = random.randrange(0, 90040)
    _female_name_seed = random.randrange(0, 90024)
    while _last_name is None:
        try:
            if gender == 'f':
                _last_name = female_names[_female_name_seed]
            else:
                _last_name = male_names[_male_name_seed]
        except:
            _male_name_seed += 1
            _female_name_seed += 1

    _random = random.randrange(0, 100)
    if _random < ucase:
        gen_name['given_name'] = _last_name
        gen_name['case'] = 'u'
    elif _random > 100 - lcase:
        gen_name['given_name'] = _last_name.swapcase()
        gen_name['case'] = 'l'
    else:
        gen_name['given_name'] = _last_name.title()
        gen_name['case'] = 'p'
    gen_name['gender'] = gender
    return gen_name

def gen_random_gender(bias=GENDER_BIAS):
    """Internal function to randomly generate a gender."""
    _random = random.randrange(0, 99)
    if _random <= bias:
        return 'f'
    else:
        return 'm'


def gen_full_name(gender=None, gender_bias=GENDER_BIAS,
                  given_names=1, randomize_name_count=True,
                  compound_name_level=101):
    """Generates a full name, including randomizing the name count and
    randomly including maiden names."""
    name = {}
    gns = []
    maiden_name = False
    compound_name = False
    if not gender:
        name['gender'] = gen_random_gender(gender_bias)
    else:
        name['gender'] = gender

    compound_name = random.randrange(1, 100) > compound_name_level

    surname = gen_last_name(compound_name=compound_name)
    name['surname'] = surname['last_name']
    name['first_to_last'] = surname['last_name']
    name['last_then_first'] = surname['last_name'] + ','

    if randomize_name_count:
        gnc = random.randrange(1, 100)
        if gnc < 70:
            given_names = 1
        elif gnc >= 70 and gnc <= 90:
            given_names = 2
            if gender == 'f':
                maiden_name = True
        elif gnc > 90 and gnc < 100:
            given_names = 2
        elif gnc == 100:
            given_names = 3
    names_list = "" # used to store the names.
    for name_count in range(given_names):
        if maiden_name and name_count > 0:
            #print 'Maiden'
            new_maiden_last_name = gen_last_name(compound_name=False)
            new_name = {'given_name' : new_maiden_last_name['last_name'], 
                               'case' : None, 'gender' : None, 
                               'ordinal' : name_count + 1}
        else:
            new_first_name = gen_first_name(gender=name['gender'])
            new_name = {'given_name' : new_first_name['given_name'], 
                               'case' : None, 'gender' : name['gender'], 
                               'ordinal' : name_count + 1}
        gns.append(new_name)
        names_list = names_list + ' ' + new_name['given_name']
    name['first_to_last'] = names_list + ' ' + name['surname']
    name['last_then_first'] = name['surname'] + ', ' + names_list.strip()
    name['given_names'] = gns
    gns = []
    return name

def gen_random_email():
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com',
               'icloud.com', 'aol.com', 'outlook.com']

    noun_len = len(word_lists.nouns)
    noun = word_lists.nouns[random.randrange(0, noun_len-1)]

    adj_len = len(word_lists.adjectives)
    adjective = word_lists.adjectives[random.randrange(0, adj_len-1)]

    domain = domains[random.randrange(0, len(domains) - 1)]
    account = '.'.join([adjective, noun]) + '@' + domain
    return account


def gen_personal_email(first_name, last_name):
    """Generates a random email address based on the first and last names."""
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com',
               'icloud.com', 'aol.com', 'outlook.com']

    domain_seed = random.randrange(0, len(domains))

    first_seed = random.randrange(0, 2)
    account = ''
    if first_seed == 0:
        account = '{0}.{1}@'.format(first_name, last_name)
    elif first_seed == 1:
        account = '{0}{1}@'.format(first_name[:1], last_name)
    else:
        account = '{0}{1}@'.format(first_name, last_name[:1])

    return account + domains[domain_seed]

def gen_address(state=None):
    """Generates a random address for the specified state."""
    if state:
        if state in STATE_ADDRESS_LIST:
            address_list_length = len(STATE_ADDRESS_LIST[state])
            state_seed = random.randrange(0, address_list_length - 1)
            # print(state_addresses[state])
            return STATE_ADDRESS_LIST[state][state_seed]
        else:
            raise ValueError('Unknown State Code')
    else:
        _random_state = random.randrange(0, len(STATE_CODE_LIST))
        state = STATE_CODE_LIST[_random_state]

        random_seed = random.randrange(0, len(STATE_ADDRESS_LIST[state]))
        return STATE_ADDRESS_LIST[state][random_seed]

def gen_employer(state):
    """Returns a random employer for the specified state."""
    # print(config.pickle_path)
    pkf = open(config.pickle_path +'employers.pkl', "rb")

    employers = pickle.load(pkf)
    pkf.close()

    sublist = [employer for employer in employers if employer['state'] == state]
    seed = random.randrange(0, len(sublist))
    return sublist[seed]

def gen_business_email(first, last, company_name):
    """Generates a business email address based on the persons name and employer."""
    company_fixed = company_name.replace('&', ' ').replace('  ', ' ')
    company_parts = company_fixed.split()
    if len(company_parts) > 3:
        company_domain = company_parts[0] + company_parts[1] #+ y[2]
    elif len(company_parts) > 1:
        company_domain = "".join([part for part in company_parts if part != company_parts[len(company_parts) - 1]])
    else:
        company_domain = company_parts[0]
    company_domain_fixed = company_domain.replace(", Inc.", "").replace("Inc.", "").replace("Inc", "").replace('/', '').replace('|', '').replace(',', '').replace(';', '').replace("'", "").strip()
    if len(company_domain_fixed) > 30:
        company_domain_fixed = company_domain_fixed[:20]
    email = gen_personal_email(first, last)
    email = email.split('@')[0] + '@' + company_domain_fixed + '.com'
    email = email.replace('..', '.')
    return email

def gen_dates(birth_year=None):
    """Generates a set of dates.  Passing birth_year ensures dates are chronological."""
    birthdate = None
  

    if birth_year:
        byear = random.randrange(birth_year - 5, birth_year + 5)
    else:
        byear = random.randrange(1944, 1992)
    birthdate = datetime.date(byear, random.randrange(1, 12), random.randrange(1, 28))

    wyear = random.randrange(byear + 18, byear + 35)

    if wyear > 2012:
        wyear = 2012

    wedding = datetime.date(wyear, random.randrange(1, 12), random.randrange(1, 28))

    results = {'birth' : birthdate, 'wedding' : wedding}

    return results

def gen_financials():
    """Generates a random set of net worth, income and liquid asset data."""
    net_worth = random.randrange(5, 33) * 10000
    liquid_assets = net_worth / random.randrange(1, 10)
    annual_income = random.randrange(7, 42) * 5000

    financials = {'net_worth' : net_worth, 'liquid_assets' : liquid_assets,
                  'annual_income' : annual_income}

    return financials

def gen_phone_number():
    """Returns a random phone number."""
    area_code = random.randrange(100, 799)
    phone_1 = random.randrange(100, 999)
    phone_2 = random.randrange(1000, 9999)
    return str(area_code) + str(phone_1) + str(phone_2)

def gen_ssn(region = False):
    """Generates a random SSN number using a xxx-xx-xxxx mask."""   
    if not region:
        part_1 = random.randrange(100, 799)
    else:
        part_1 = region
    part_2 = random.randrange(10, 99)
    part_3 = random.randrange(1000, 9999)
    return str(part_1) + "-" + str(part_2) + "-" + str(part_3)

def gen_bank_account():
    """Returns a random bank account number between 9 and 14 characters in 
    length.  Some values have an appeneded text string."""
    num_len = random.randrange(7, 12)
    upper_range = int(math.pow(10, num_len)-1)
    account_number = random.randrange(1, upper_range)
    first_letter_seed = 22  #the percentage of account numbers with 1-2 initial letters.
    account_number_seed = random.randrange(0, 99)
    if account_number_seed <= first_letter_seed:
        account_number = 'AB' + str(account_number)
    return str(account_number)

def gen_drivers_license():
    """Returns a random number between 7 and 12 characters in length."""
    num_len = random.randrange(7, 12)
    upper_range = int(math.pow(10, num_len)-1)
    account_number = random.randrange(1, upper_range)
    first_letter_seed = 22  #the percentage of account numbers with 1-2 initial letters.
    seed_value = random.randrange(0, 99)
    if seed_value <= first_letter_seed:
        account_number = random.choice(string.ascii_letters).upper() + str(account_number)
    if seed_value < (first_letter_seed / 2):
        account_number = random.choice(string.ascii_letters).upper() + str(account_number)
    return str(account_number)

def _luhn_total(num):
    digits = [int(x) for x in str(num)]
    total = sum(digits[-1::-2])
    for digit in digits[-2::-2]:
        digit *= 2
        if digit > 9: digit -= 9
        total += digit
    return total

def luhn_check(num):
    """Returns true if the number has a valid luhn checksum"""
    return _luhn_total(num) % 10 == 0

def luhn_gen(num):
    """Returns the check digit for the given number"""
    return (_luhn_total(num + "0") * 9) % 10

def _cc_range(ranges):
    """Generates a flat list of numbers from a list of individual numbers
        and (start, stop) pairs."""
    o_range = []
    for r in ranges:
        try:
            start, end = r
            o_range.extend(list(range(start, end+1)))
        except TypeError:
            o_range.append(r)
    return o_range 

def cc(name, BINs, lengths, checksum=True):
    BINs = _cc_range(BINs)
    lengths = _cc_range(lengths)
    def _cc_gen():
        card_len = random.choice(lengths)
        BIN = str(random.choice(BINs))
        account_num_len = card_len - len(BIN)
        if checksum:
            account_num_len -= 1
        account_num = random.randrange(0, (10 ** (account_num_len + 1)) - 1)
        card_num = BIN + str(account_num)
        if checksum:
            card_num += str(luhn_gen(card_num))
        return card_num
    _cc_gen.__name__ = name
    return _cc_gen

# All information from: https://en.wikipedia.org/wiki/Payment_card_number
CC_TYPES_INACTIVE = [
    cc("Bankcard", [5610, (560221, 560225)], [16]),
    cc("Diners Club enRoute", [2014, 2149], [15], checksum=False),
    cc("Laser", [6304, 6706, 6771, 6709], [(16, 19)]),
    cc("MasterCard", [(2221, 2720)], [16]),
    cc("Solo", [6334, 6767], [16, 18, 19]),
    cc("Switch", [4903, 4905, 4911, 4936, 564182, 633110, 6333, 6759], [16, 18, 19])
]

CC_TYPES_ACTIVE = [
    cc("American Express", [34, 37], [16]),
    cc("China UnionPay", [62], [(16, 19)]),
    cc("Diners Club Carte Blanche", [(300, 305)], [14]),
    cc("Diners Club International", 
            [(300, 305), 309, 36, 38, 39], [14]),
    cc("Discover Card",
            [6011, (622126, 622925), (644, 649), 65], [16, 19]),
    cc("InterPayment", [636], [(16, 19)]),
    cc("InstaPayment", [(637,639)], [16]),
    cc("JCB", [(3528, 3589)], [16]),
    cc("Maestro", [50, (56, 69)], [(12, 19)]),
    cc("Dankort", [5019], [16]),
    cc("Dankort + Visa", [4, 4175, 4571], [16]),
    cc("NSPK MIR", [(2200, 2204)], [16]),
    cc("MasterCard", [(51, 55)], [16]),
    cc("Visa", [4], [13, 16, 19]),
    cc("UATP", [1], [15]),
    cc("Verve", [(506099, 506198), (650002, 650027)], [16, 19]),
    cc("CARDGUARD EAD BG ILS", [5392], [16])
]

# There could be many better sampling methods, for example sampling according
# to popular distribution of cards. I imagine there are many more visas than
# "InterPayment" cards, at least in the U.S.
# Even sampling according to the possible number of unique cards would probably
# be better.
def gen_credit_card_number():
    """Returns a random 16 digit numeric value, common to Visa style 
       credit card numbers."""
    return random.choice(CC_TYPES_ACTIVE)()


if __name__ == '__main__':
    STATE_CODE_LIST_LENGTH = len(STATE_CODE_LIST)
            
    for i in range(3):
        random_state = STATE_CODE_LIST[random.randrange(0, STATE_CODE_LIST_LENGTH)]
        print(gen_bank_account())
        print(gen_credit_card_number())
        print(gen_drivers_license())
        print(gen_ssn())
        print(gen_financials())
        test_first_name = gen_first_name()
        test_last_name = gen_last_name()
        print(test_first_name)
        print(test_last_name)
        company = gen_employer(random_state)
        print("Company:", company)
        print(gen_business_email(test_first_name['given_name'], 
              test_last_name['last_name'], company['company']))
        print("Address:", gen_address(random_state))
        print("Personal Email:", gen_personal_email(test_first_name['given_name'], 
              test_last_name['last_name']))
        print("Full Name:", gen_full_name())
        print(gen_first_name(2, 2, 'f'))
        print(gen_first_name(1, 2, 'f'))
        print(gen_first_name(2, 1, 'f'))
        print(gen_first_name(1, 1, 'f'))
        print(gen_first_name(2, 2, 'm'))
        print(gen_first_name(1, 2, 'm'))
        print(gen_first_name(2, 1, 'm'))
        print(gen_first_name(1, 1, 'm'))



        print('-' * 80)

        for i in range(10):
            print(gen_random_email())
        names = {}
    for i in range(100):
        foo = gen_first_name()
        if foo['gender'] in names:
            names[foo['gender']] += 1
        else:
            names[foo['gender']] = 1

    import pprint
    pprint.pprint(names)



