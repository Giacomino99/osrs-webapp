''' Endponts for OSRS Calculator application '''

from datetime import datetime
from flask import Flask, request, make_response, render_template
import requests
import json
import os
import datetime
import time
from pprint import pprint

from recipies import POTIONS, POTION_RECIPIES

app = Flask(__name__, template_folder = 'templates')
HEADER = {'user-agent' : 'OSRS Profit Calculator, Giacomino#6416'}
API_URL = 'http://prices.runescape.wiki/api/v1/osrs'

ITEM_MAP = {}
ITEM_PRICES = {}

# pprint(POTION_RECIPIES, width = 160)

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    update_files()
    load_data()
    html = render_template('index.html', potions = get_potion_info())
    response = make_response(html)
    print(get_price('guam leaf'))
    return response

def update_files(update_map = False):
    # Update item mapping (does not change often)
    if not os.path.exists('mapping.json') or update_map:
        latest_map = requests.get(API_URL + '/mapping', headers = HEADER)
        ITEM_MAP = {}
        for item in latest_map.json():
            ITEM_MAP[item['name'].upper()] = item
        print('REQUEST FOR UPDATED MAPPING')
        with open('mapping.json', 'w') as f:
            json.dump(latest_map.json(), f)
        with open('mapping2.json', 'w') as f:
            json.dump(ITEM_MAP, f)

    latest_time = 0 if not os.path.exists('latest.json') else os.path.getctime('latest.json')
    if latest_time + 60 < time.time():
        latest_prices = requests.get(API_URL + '/latest', headers = HEADER)
        ITEM_PRICES = latest_prices.json()['data']
        print('REQUEST FOR UPDATED PRICES')
        with open('latest.json', 'w') as f:
            json.dump(ITEM_PRICES, f)

def load_data():
    global ITEM_MAP
    global ITEM_PRICES
    if not ITEM_MAP:
        with open('mapping2.json', 'r') as f:
            ITEM_MAP = json.load(f)
    if not ITEM_PRICES:
        with open('latest.json', 'r') as f:
            ITEM_PRICES = json.load(f)

def get_price(name):
    if name.upper() in ITEM_MAP:
        item_id = str(ITEM_MAP[name.upper()]['id'])
        return ITEM_PRICES[item_id]['high']
    return -1

def tradable(name):
    if name.upper() in ITEM_MAP:
        return True
    return False

def get_potion_info():
    out = []
    for potion in POTIONS:
        data = []
        if tradable(potion):
            data.append(potion)
            data.append(get_price(potion))
            data.extend([0,0,0])
            out.append(data)
        elif tradable(potion + '(1)'):
            data.append(potion)
            data.append(get_price(potion + '(1)'))
            data.append(get_price(potion + '(2)')//2)
            data.append(get_price(potion + '(3)')//3)
            data.append(get_price(potion + '(4)')//4)
            out.append(data)

    return out