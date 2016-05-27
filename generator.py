from MockData.names_list import last_names, female_names, male_names
import random
import pprint
import json
import MockData.config as config
import pickle
import datetime
import unicodedata
import string
import random
from MockData.config import source_path, data_path

pp = pprint.PrettyPrinter(indent=4)

GENDER_BIAS = 53
last_name = {'last_name' : None, 'case' : None }
first_name = {'given_name' : None, 'case' : None, 'gender' : None, 'ordinal' : 0  }
full_name = { 'first_to_last' : None, 'last_then_first' : None,  'gender' : None,
              'given_names' : [], 'surname' : None }


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

stateCodeList = [
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

sa = open(data_path + 'state-address.json')
state_addresses = json.load(sa)


def gen_last_name(ucase=2, lcase=2, 
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
        gen_name['last_name'] =  ln.title()
        gen_name['case'] = 'p'
    gen_name['seed'] = x
    x = None
    return gen_name

def gen_first_name(ucase=2, lcase=2, gender=False):
    gen_name = {}
    ln = None
    x = random.randrange(0, 90040)
    while ln is None:
        try:
            if gender == 'f':
                ln = female_names[x]
            else:
                ln = male_names[x]
        except:
            x = x + 1
            pass
    u = random.randrange(0, 100)
    if u < ucase:
       gen_name['given_name'] = ln
       gen_name['case'] = 'u'
    elif u > 100 - lcase:
        gen_name['given_name'] = ln.swapcase()
        gen_name['case'] = 'l'
    else:
        gen_name['given_name'] = ln.title()
        gen_name['case'] = 'p'

    return gen_name


def gen_full_name(case=None, gender=None, gender_bias=GENDER_BIAS, 
                  given_names=1, randomize_name_count = True):
    name = {}
    gns = []
    maiden_name = False
    compound_name = False
    if not gender:
        g = random.randrange(0, 99)
        if g <= gender_bias:
            name['gender'] = 'f'
        else:
            name['gender'] = 'm'
    else:
        name['gender'] = gender
    cn = random.randrange(1, 100)
    if cn > 95:
        compound_name = True
    gn = gen_last_name(compound_name = compound_name)
    name['surname'] = gn['last_name']

    name['first_to_last'] = gn['last_name']
    name['last_then_first'] = gn['last_name'] + ','


    if randomize_name_count:
        gnc = random.randrange(1, 100)
        if gender == 'm':
            if gnc < 50:
                given_names = 1
            elif gnc >= 50 and gnc <= 99:
                given_names = 2
            elif gnc == 100:
                given_names = 3
        else:
            if gnc < 70:
                given_names = 1
            elif gnc >= 70 and gnc <= 90:
                given_names = 2
                maiden_name = True
            elif gnc > 90 and gnc < 100:
                given_names = 2
            elif gnc == 100:
                given_names = 3
    names_list = "" # used to store the names.
    for x in range(given_names):
        if maiden_name and x > 0:
            #print 'Maiden'
            mn = gen_last_name(compound_name = False)
            nn =  {'given_name' : None, 'case' : None, 'gender' : None, 'ordinal' : 0  }
            nn['given_name'] = mn['last_name']
            nn['ordinal'] = x + 1
        else:
            nn = gen_first_name(gender=name['gender'])
            nn['ordinal'] = x + 1
        gns.append(nn)
        names_list = names_list + ' ' + nn['given_name']
    name['first_to_last'] = names_list + ' ' + name['surname']
    name['last_then_first'] = name['surname'] + ', ' + names_list.strip()
    name['given_names'] = gns
    gns = []
    return name

def gen_personal_email(first_name, last_name):
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 
               'icloud.com', 'aol.com', 'outlook.com']

    x = random.randrange(0, len(domains))

    f = random.randrange(0, 2)
    n = ''
    if f == 0:
        n = '{0}.{1}@'.format(first_name, last_name)
    elif f == 1:
        n = '{0}{1}@'.format(first_name[:1], last_name)
    else:
        n = '{0}{1}@'.format(first_name, last_name[:1])

    return n + domains[x]

def gen_address(state=None):
    # pkf = open(config.pickle_path + 'addresses.pkl', 'rb')
    # addresses = pickle.load(pkf)
    # pkf.close()
    # sublist = [address for address in addresses
    #         if address['state'] == state]
    # x = random.randrange(0, len(sublist))
    if state:
        if state in state_addresses:
            sc = len(state_addresses[state])
            x = random.randrange(0, sc - 1)
            # print(state_addresses[state])
            return state_addresses[state][x]
        else:
            raise ValueError('Unknown State Code')
    else:
        scl = random.randrange(0, len(stateCodeList))
        state = stateCodeList[scl]

        x = random.randrange(0, len(state_addresses[state]))
        return state_addresses[state][x]

    return address

def gen_employer(state):
    print(config.pickle_path)
    pkf = open(config.pickle_path +'employers.pkl', "rb")

    employers = pickle.load(pkf)
    pkf.close()

    sublist = [employer for employer in employers
            if employer['state'] == state]
    x = random.randrange(0, len(sublist))
    return sublist[x]

def gen_business_email(first, last, company):
    company = company.replace('&', ' ')
    company = company.replace('  ', ' ')
    y = company.split()
    if len(y) > 3:
        company = y[0] + y[1] #+ y[2]
    elif len(y) > 1:
        company = "".join([part for part in y if part != y[len(y) - 1]])
    else:
        company = y[0]
    company = company.replace(", Inc.", "").replace("Inc." , "").replace("Inc", "").replace('/', '')
    company = company.replace('|', '').replace(',', '').replace(';', '').replace("'", "").strip()
    if len(company) > 30:
        company = company[:20]
    email = gen_personal_email(first, last)
    email = email.split('@')[0] + '@' + company + '.com'
    email = email.replace('..', '.')
    return email

def gen_favorites(gender="f"):
    cuisine = ''
    dessert = ''
    music = ''
    snack = ''
    hobby = ''
    religion = ''
    drink = ''

    cuisines = ['American', 'Italian', 'Mexican', '???', 'French', 'Japanese', 
                'Chinese', 'italian', 'Tex/Mex', 'Seafood', 'anything', 
                'mexican', '', '', 'none', '' ]
    desserts = ['Apple Pie', 'Ice Cream', '', '', '', '', 'Cheesecake', 
                'pumpkin pie', 'Yogurt', 'Fruit', 'Chocolate Cake']
    music_genres = ['Classical', 'jazz', 'Jazz', 'country', 'Country/Western', 
                    'punk', 'punk-rock', 'disco', '', '', '', 'Pop', 'rock', 
                    'Rock and Roll', '', 'Hip-Hop']
    religions = ['', '', '', '', '', '', 'Baptist', 'Catholic', 'Methodist', 
                 'Jewish', 'atheist', 'None', 'Baptist', 'Lutheran', 'Unitarian', 
                 'Presbyterian', 'catholic', 'Buddhist' ]
    snacks = ['peanuts', 'twinkies', 'Gummy Bears', "M&M's", 'pretzels', '', 
              '', '', '', 'Chocolate Chip Cookies', 'Oreo''s', 'Swedish Fish', 
              'Goldfish', 'Chocolate', 'Chocolate', 'chocolate', 'Candy', 
              'Snickers', 'Apples', 'Bananas', 'banana', 'chips', 'almonds' ]
    drinks = ['Coffee', 'Coffee', 'coffee', 'tea', 'Tea', 'Red Bull', 'Monster',
              '', '', '', 'Coke', 'Coke Zero', 'Pepsi', 'Diet Coke', 'Coke', 
              'Pepsi', 'Water', 'water', 'Orange Juice', 'Espresso', 'Ice Tea', 
              'Lemonade']
    cuisine = cuisines[random.randrange(0, len(cuisines))]
    dessert = desserts[random.randrange(0, len(desserts))]
    music = music_genres[random.randrange(0, len(music_genres))]
    religion = religions[random.randrange(0, len(religions))]
    snack = snacks[random.randrange(0, len(snacks))]
    drink = drinks[random.randrange(0, len(drinks))]

    favorites = {'cuisine' : cuisine, 'dessert' : dessert, 
                 'music' : music, 'snack' : snack, 'hobby' : hobby, 
                 'religion' : religion, 'drink' : drink }

    return favorites

def gen_dates(birth_year=None):
    birthdate = None
    wedding = ''

    if birth_year:
        byear = random.randrange(birth_year - 5, birth_year + 5)
    else:
        byear = random.randrange(1944, 1992)
    birthdate = datetime.date(byear, random.randrange(1,12), random.randrange(1,28))

    wyear = random.randrange(byear + 18, byear + 35)

    if wyear > 2012: wyear  = 2012

    wedding = datetime.date(wyear, random.randrange(1,12), random.randrange(1, 28))

    results = {'birth' : birthdate, 'wedding' : wedding }

    return results

def gen_financials():
    net_worth = random.randrange(5, 33) * 10000
    liquid_assets = net_worth / random.randrange(1, 10)
    annual_income = random.randrange(7, 42) * 5000

    financials = {'net_worth' : net_worth, 'liquid_assets' : liquid_assets, 'annual_income' : annual_income }

    return financials

def gen_school(state):
    colleges = pickle.load(open(config.pickle_path + 'colleges.pkl', 'rb'))
    state_colleges = colleges[state]
    if state_colleges:
        return state_colleges[random.randrange(0, len(state_colleges))]

def gen_phone_number():
    area_code = random.randrange(100, 799)
    phone1 = random.randrange(100, 999)
    phone2 = random.randrange(1000, 9999)
    return str(area_code) + str(phone1) + str(phone2)
    
def gen_SSN():
    area_code = random.randrange(100, 799)
    phone1 = random.randrange(10, 99)
    phone2 = random.randrange(1000, 9999)
    return str(area_code) + "-" + str(phone1) + "-" + str(phone2)

def gen_bank_account():
    num_len = random.randrange(7, 12)
    x = 1
    for i in range(num_len):
        x = x * 10
    x = x - 1
    account_number = random.randrange(1, x)
    first_letter_seed = 22  #the percentage of account numbers with 1-2 initial letters.
    f = random.randrange(0, 99)
    if f <= first_letter_seed:
        account_number = 'AB' + str(account_number)
    return str(account_number)

def gen_drivers_license():
    num_len = random.randrange(7, 12)
    x = 1
    for i in range(num_len):
        x = x * 10
    x = x - 1
    account_number = random.randrange(1, x)
    first_letter_seed = 22  #the percentage of account numbers with 1-2 initial letters.
    f = random.randrange(0, 99)
    if f <= first_letter_seed:
        account_number = random.choice(string.ascii_letters).upper() + str(account_number)
    if f < (first_letter_seed / 2):
        account_number = random.choice(string.ascii_letters).upper() + str(account_number)
    return str(account_number)

def gen_credit_card_number():
    return str(random.randrange(1000000000000000, 9999999999999999))

if __name__ == '__main__':
    # print('10 random names')
    # for i in range(10):
    #     print(gen_full_name())    
    # print('10 names matching distribution')
    for i in range(10):
        print(gen_bank_account())
