import csv
import codecs
import sys
from pprint import pprint
import json
import hashlib
from config import source_path, pickle_path
import time
import datetime

country_list = {}
addresses = []

def get_hash(val):
    hash_object = hashlib.sha256(val.encode('utf-8'))
    return hash_object.hexdigest()

def count_names(data_list, data_value):
    if data_value in data_list:
        data_list[data_value] += 1
    else:
        data_list[data_value] = 1
    return data_list

def cleanse_street1(val):
    suites = [", SUITE", ", STE", " Ste ", ", #", ', Suite', ' STE ']
    for suite in suites:
        if suite in val:
            return val.split(suite)[0]
    return val

def detect_PO_Box(val):
    if val.upper().startswith("PO BOX "):
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

def load_FOIA_Participants_FY_2010():
    load_count = 0
    skip_count = 0
    with codecs.open(source_path + 'FOIA_Participants_FY_2010.csv', 
                    encoding = 'ISO-8859-2') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Country'] == 'United States':
                # country_list = count_names(country_list, row['State Name'])
                address = {'street1' : cleanse_street1(row['Address']), 
                            'city' : row['City'], 
                            'state_code' :row.get('State Code', ''), 
                            'postal_code' : row['ZIP Code'], 
                            'country' : row['Country']}

                if address not in addresses:
                    addresses.append(address)
                    load_count += 1
                else:
                    skip_count += 1

    return (load_count, skip_count)

def load_churches(skip_PO_boxes = True):
    load_count = 0
    skip_count = 0
    with codecs.open(source_path + 'churches.csv', encoding = 'windows-1252') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address = {'street1' : cleanse_street1(row['Street1']), 
                        'city' : row['City'], 
                        'state_code' :row.get('State Code', ''), 
                        'postal_code' : row['Zip']}

            if address not in addresses:
                if skip_PO_boxes & detect_PO_Box(row["Street1"]):
                    skip_count += 1
                else:
                    addresses.append(address)
                    load_count += 1
            else:
                skip_count += 1

    return (load_count, skip_count)

def load_hotels():
    load_count = 0
    skip_count = 0
    with codecs.open(source_path + 'hotels.csv', 
            encoding = 'ISO-8859-2') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count_names(country_list, row['Country_Code'])
            if row['Country_Code'] == 'US':
                address = {'street1' : cleanse_street1(row['Street1']), 
                            'city' : row['City'], 
                            'state_code' :row.get('State', ''), 
                            'postal_code' : row['PostalCode'], 
                            'country' : row['Country_Code']}
                if address not in addresses:
                    addresses.append(address)
                    load_count += 1
                else:
                    skip_count += 1

    return (load_count, skip_count)

def load_hospital_data():
    load_count = 0
    skip_count = 0
    with open(source_path + 'hospital-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            address = {'street1' : cleanse_street1(row['Address 1']), 
                        'city' : row['City'], 
                        'state_code' :row.get('State', ''), 
                        'postal_code' : row['ZIP Code']
                        }
            if address not in addresses:
                addresses.append(address)
                load_count += 1
            else:
                skip_count += 1

    return (load_count, skip_count)

addresses = load_addresses(addresses, source_path + 'address.json')
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

t1 = time.time()
print('Loading churches.csv')
counts = load_churches()
print('source_count: ', len(addresses))
print('load_count: ', str(counts[0]))
print('skip_count: ', str(counts[1]))
t2 = time.time()
print('load time: ', str(t2-t1))

f = open(source_path + 'address.json', 'w+')
json.dump(addresses, f)
f.close()