import configparser
from webbrowser import get
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import json, requests
import time
import pandas as pd
from consolemenu import *
from consolemenu.items import *
from consolemenu.format import *



def initial_setup():

    function_item = FunctionItem("Setup", write_auth, None, None, None, should_exit=True)
    menu = ConsoleMenu("Setup", "Time to setup before you can use KFoSs-PC!", None, formatter=menu_format)
    menu.append_item(function_item)
    menu.show()


def write_auth():
    config = configparser.ConfigParser()
    global auth_name
    auth_name = input("Please input your username:")
    global auth_pass
    auth_pass = input("Please input your password:")
    get_auth_token()

    config['auth'] = {
        'c_i': auth_name,
        'c_s': auth_pass, 
    }

    config['token'] = {
        'just_token': just_token,
        'token_exp': token_exp
    }

    user_zip = input('Please input your ZIP code:')
    
    user_location = get_locations(user_zip, "Kroger", 1)
    global storenumber
    storenumber = user_location.get("data")[0].get("locationId")
    storename = user_location.get("data")[0].get("name")

    config['location'] = {
        'location_id': storenumber,
        'location_name': storename
    }


    
    '''
    nums = 0

    while nums < 15:
        storenumber = user_location.get("data")[nums].get("locationId")
        storename = user_location.get("data")[nums].get("name")
        print(storenumber + ' - ' + storename)
        nums = nums + 1
    '''


    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def get_locations(zip, chain, limit):
    heads = {
    "Accept": "application/json\\",
    "Authorization": "Bearer "+just_token,
    }

    paras = {
    "filter.zipCode.near": zip,
    "filter.chain": chain,
    "filter.limit": limit,
    }  

    return requests.get("https://api.kroger.com/v1/locations", params=paras, headers=heads).json()


def get_auth_token():
    #Oauthlib client id, secret, and scope
    auth = HTTPBasicAuth(auth_name, auth_pass)
    client = BackendApplicationClient(client_id=auth_name, scope='product.compact')
    oauth = OAuth2Session(client=client, scope='product.compact')

    #Fetch token
    full_token = oauth.fetch_token(token_url='https://api.kroger.com/v1/connect/oauth2/token', auth=auth)

    #Grab access token from returned dict
    global just_token
    just_token = full_token.get("access_token")

    #Grab espiration time from returned dict (30 min default)
    global token_exp
    token_exp = full_token.get("expires_at")


def search_items():

    if (float(token_exp) - time.time()) < 300:
        get_auth_token
        list_products()
    else:
        list_products()


def list_products():
    term = input("Input the item you are looking for:")
    product = get_products(term, 1, storenumber)
    description = product.get("data")[0].get("description")
    size = product.get("data")[0].get("items")[0].get("size")
    regular_price = product.get("data")[0].get("items")[0].get("price").get("regular")

    menu = ConsoleMenu("Product menu", "Products!")

    command_item = CommandItem(description, "touch hello.txt")
    menu.append_item(command_item)

    menu.show()

    

def get_products(searchterm, limit, locID):
    heads1 = {
    "Accept": "application/json\\",
    "Authorization": "Bearer "+just_token,
    }

    paras1 = {
    "filter.term": searchterm,
    "filter.limit": limit,
    "filter.locationId": locID,
    }
    

    return requests.get("https://api.kroger.com/v1/products", params=paras1, headers=heads1).json()


def historical_prices():
    pass


def possible_closeouts():
    pass








menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_OUTER_LIGHT_INNER_BORDER)

readconfig = configparser.ConfigParser()

if readconfig.read('config.ini') != []:
    auth_name = readconfig.get('auth', 'c_i')
    auth_pass = readconfig.get('auth', 'c_s')
    token_exp = readconfig.get('token', 'token_exp')
    just_token = readconfig.get('token', 'just_token')
    storenumber = readconfig.get('location', 'location_id')
    get_auth_token()
else:
    initial_setup()



menu = ConsoleMenu("Main menu", "Let's find some prices!")

command_item = CommandItem("Run a console command", "touch hello.txt")
search_for_items = FunctionItem("Search for items", search_items)
view_historical_prices = FunctionItem("View historical prices", historical_prices)
view_possible_closeouts = FunctionItem("View possible closeouts", possible_closeouts)
function_item = FunctionItem("Setup", write_auth, None, None, None, should_exit=True)

menu.append_item(search_for_items)
menu.append_item(view_historical_prices)
menu.append_item(view_possible_closeouts)
menu.append_item(command_item)
menu.append_item(function_item)
menu.show()