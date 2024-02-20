import csv
import json
import random


class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0


# mouse = Mouse()


def convert_csv_to_json():
    with open('geo.csv', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    with open('geo.json', 'w', encoding="utf-8") as f:
        json.dump(rows, f)


def read_json():
    return json.load(open('geo.json', encoding="utf-8"))


def get_target_locations() -> str:
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


def get_window_characteristics(driver):
    win_upper_bound = driver.execute_script('return window.pageYOffset')
    win_height = driver.execute_script(
        'return document.documentElement.clientHeight')
    win_lower_bound = win_upper_bound + win_height
    return win_upper_bound, win_lower_bound


def get_location_characteristics(web_element):
    elem_top_bound = web_element.location.get('y')
    elem_height = web_element.size.get('height')
    elem_lower_bound = elem_top_bound + elem_height
    return elem_top_bound, elem_lower_bound
