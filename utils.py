import csv
import json
import random


def convert_csv_to_json():
    with open('geo.csv') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    with open('geo.json', 'w') as f:
        json.dump(rows, f)


def read_json():
    return json.load(open('geo.json'))


def get_target_locations():
    geo = read_json()
    item = get_random_geo(geo, p_spb=0.5, p_moscow=0.3, p_other=0.2)
    city = item['city']
    street = item['street']
    return f'{street} {city}'


def get_random_geo(data, p_spb=0.5, p_moscow=0.3, p_other=0.2):
    while True:
        obj = random.choice(data)
        if obj['region'] == 'Санкт-Петербург':
            return obj
        elif obj['region'] in ['Москва', 'Москвская область']:
            return obj
        else:
            return get_random_geo(data, p_spb, p_moscow, p_other)
