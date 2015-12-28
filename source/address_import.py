import csv
import codecs
import sys
from pprint import pprint
import json
import hashlib
from config import source_path, pickle_path, data_path
import time
import datetime

state_count = {}
addresses = []

state_list = {'DC': 'District of Columbia', 
    'NH': 'New Hampshire', 'VT': 'Vermont', 'OH': 'Ohio', 'MA': 'Massachusetts', 
    'NC': 'North Carolina', 'AL': 'Alabama', 'PR': 'Puerto Rico', 
    'IL': 'Illinois', 'MD': 'Maryland', 'NE': 'Nebraska', 'MS': 'Mississippi', 
    'NY': 'New York', 'UT': 'Utah', 'IN': 'Indiana', 'IA': 'Iowa', 'NV': 'Nevada', 
    'ME': 'Maine', 'WY': 'Wyoming', 'CA': 'California', 'NJ': 'New Jersey', 'HI': 
    'Hawaii', 'TX': 'Texas', 'CT': 'Connecticut', 'OK': 'Oklahoma', 'MN': 'Minnesota', 
    'KS': 'Kansas', 'FL': 'Florida', 'OR': 'Oregon', 'MO': 'Missouri', 'SC': 'South Carolina', 
    'ID': 'Idaho', 'DE': 'Delaware', 'TN': 'Tennessee', 'VA': 'Virginia', 'MT': 'Montana', 
    'WA': 'Washington', 'WI': 'Wisconsin', 'AZ': 'Arizona', 'MI': 'Michigan', 
    'AR': 'Arkansas', 'SD': 'South Dakota', 'KY': 'Kentucky', 'CO': 'Colorado', 
    'ND': 'North Dakota', 'NM': 'New Mexico', 'PA': 'Pennsylvania', 'WV': 'West Virginia', 
    'RI': 'Rhode Island', 'AK': 'Alaska', 'LA': 'Louisiana', 'GA': 'Georgia'}

def get_hash(val):
    hash_object = hashlib.sha256(val.encode('utf-8'))
    return hash_object.hexdigest()

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

def cleanse_street1(val):
    suites = [", SUITE", ", STE", " Ste ", ", #", ', Suite', ' STE ']
    new_val = val
    for suite in suites:
        if suite in val:
            new_val = val.split(suite)[0]

    if ' RM ' in new_val:
        new_val = new_val.split(" RM ")[0]
    return new_val

def detect_PO_Box(val):
    if val.upper().strip().startswith("PO BOX "):
        return True
    else:
        return False

def load_addresses(addresses, data_file_path):
    addresses = []
    try:
        f = open(data_file_path)
        addresses = json.load(f)
    except:
        addresses = []
    return addresses    

def append_address(address):
    if address['state_code'] not in addresses:
        return False
    if detect_PO_Box(address['state_code']):
        return False
    address['street1'] = cleanse_street1(address['street1'])
     
    if address not in addresses[address['state_code']]:
        addresses[address['state_code']].append(address)
        count_names(state_count, address['state_code'])
        return True
    else:
        return False


def load_FOIA_Participants_FY_2010():
    load_count = 0
    skip_count = 0
    with codecs.open(source_path + 'FOIA_Participants_FY_2010.csv', 
                    encoding = 'ISO-8859-2') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Country'] == 'United States':
                # country_list = count_names(country_list, row['State Name'])
                address = {'street1' : cleanse_street1(row['Address'].strip()), 
                            'city' : row['City'], 
                            'state_code' :row.get('State Code', ''), 
                            'postal_code' : row['ZIP Code'], 
                            'country' : row['Country']}
                do_append = append_address(address)

                if do_append: load_count += 1
                else: skip_count += 1

    return (load_count, skip_count)

def load_churches(skip_PO_boxes = True):
    print(source_path)
    load_count = 0
    skip_count = 0
    row_count = 0
    with codecs.open(source_path + 'churches.csv', 
                    encoding = 'windows-1252') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address = {'street1' : cleanse_street1(row['Street1'].strip()), 
                        'city' : row['City'], 
                        'state_code' :row.get('State', '').strip(), 
                        'postal_code' : row['Zip']}
            do_append = append_address(address)

            if do_append: load_count += 1
            else: skip_count += 1
        
    return (load_count, skip_count)

def load_hotels():
    load_count = 0
    skip_count = 0
    with codecs.open(source_path + 'hotels.csv', 
            encoding = 'ISO-8859-2') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            if row['Country_Code'] == 'US':
                address = {'street1' : cleanse_street1(row['Street1'].strip()), 
                            'city' : row['City'], 
                            'state_code' :row.get('State', ''), 
                            'postal_code' : row['PostalCode'], 
                            'country' : row['Country_Code']}
                do_append = append_address(address)

                if do_append: load_count += 1
                else: skip_count += 1

    return (load_count, skip_count)

def load_hospital_data():
    load_count = 0
    skip_count = 0
    with open(source_path + 'hospital-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            address = {'street1' : cleanse_street1(row['Address 1']), 
                        'city' : row['City'], 
                        'state_code' :row.get('State', '').strip(), 
                        'postal_code' : row['ZIP Code']
                        }
            do_append = append_address(address)

            if do_append: load_count += 1
            else: skip_count += 1

    return (load_count, skip_count)

def load_locaddr(skip_PO_boxes = True):
    print(source_path)
    load_count = 0
    skip_count = 0
    row_count = 0
    with codecs.open(source_path + 'locaddr.csv', encoding = 'ascii') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address = {'street1' : cleanse_street1(row['LOCATION_STREET1']), 
                        'city' : row['LOCATION_CITY'], 
                        'state_code' :row.get('LOCATION_STATE', '').strip(), 
                        'postal_code' : row['LOCATION_ZIP']}
            do_append = append_address(address)

            if do_append: load_count += 1
            else: skip_count += 1
    return (load_count, skip_count)

def load_mailaddr(skip_PO_boxes = True):
    print(source_path)
    load_count = 0
    skip_count = 0
    row_count = 0
    with codecs.open(source_path + 'mailaddr.csv', encoding = 'ascii') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address = {'street1' : cleanse_street1(row['MAILING_STREET1']), 
                        'city' : row['MAILING_CITY'], 
                        'state_code' :row.get('MAILING_STATE', '').strip(), 
                        'postal_code' : row['MAILING_ZIP']}
            if address['state_code'] not in addresses:
                # print('no state: ', address['state_code'])
                continue
            if " & " in address['street1']:
                ### exclude intersections i.e. 34th & Broadway
                skip_count += 1
                continue
            do_append = append_address(address)

            if do_append: load_count += 1
            else: skip_count += 1
    return (load_count, skip_count)

addresses = {}


#### INITIAL LOAD/RELOAD
for state in state_list.items():
    addresses[state[0]] = []

#### APPEND
# addresses = load_addresses(addresses, data_path + 'state-address.json')

####

t1 = time.time()
print('Loading hospital-data.csv')
counts = load_hospital_data()
print('source_count: ', len(addresses))
print('load_count: ', str(counts[0]))
print('skip_count: ', str(counts[1]))
t2 = time.time()
print('load time: ', str(t2-t1))

t1 = time.time()
print('Loading FOIA_Participants_FY_2010.csv')
counts = load_FOIA_Participants_FY_2010()
print('source_count: ', len(addresses))
print('load_count: ', str(counts[0]))
print('skip_count: ', str(counts[1]))
t2 = time.time()
print('load time: ', str(t2-t1))

t1 = time.time()
print('Loading hotels.csv')
counts = load_hotels()
print('source_count: ', len(addresses))
print('load_count: ', str(counts[0]))
print('skip_count: ', str(counts[1]))
t2 = time.time()
print('load time: ', str(t2-t1))

# t1 = time.time()
# print('Loading churches.csv')
# counts = load_churches()
# print('source_count: ', len(addresses))
# print('load_count: ', str(counts[0]))
# print('skip_count: ', str(counts[1]))
# t2 = time.time()
# print('load time: ', str(t2-t1))

t1 = time.time()
print('Loading locaddr.csv')
counts = load_locaddr()
print('source_count: ', len(addresses))
print('load_count: ', str(counts[0]))
print('skip_count: ', str(counts[1]))
t2 = time.time()
print('load time: ', str(t2-t1))

# t1 = time.time()
# print('Loading mailaddr.csv')
# counts = load_mailaddr()
# print('source_count: ', len(addresses))
# print('load_count: ', str(counts[0]))
# print('skip_count: ', str(counts[1]))
# t2 = time.time()
# print('load time: ', str(t2-t1))


pprint(state_count)
tc = 0
for s in addresses:
    tc += len(addresses[s])
print('Total Addresses in File: ', tc)
f = open(data_path + 'state-address.json', 'w+')
json.dump(addresses, f)
f.close()