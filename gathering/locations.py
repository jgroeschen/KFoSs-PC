import requests


def get_chains(token):
    heads = {
        'Accept': 'application/json\\',
        'Authorization': 'Bearer ' + token,
    }
    chains_data = requests.get('https://api.kroger.com/v1/chains',
                               headers=heads).json()
    chains_list = []
    for i in range(len(chains_data.get('data'))):
        chains_list.append(chains_data.get('data')[i].get('name'))
    # Remove gas stations and other unusable locations
    chains_list = [e for e in chains_list if e not in (
        'AMOCO', 'BP', 'COPPS', 'COVID', 'EG GROUP', 'FRED',
        'FRESH EATS MKT', 'HARRIS TEETER FUEL',
        'HARRIS TEETER FUEL CENTER', 'HART', 'JEWELRY', 'KWIK',
        'KWIK SHOP', 'LOAF', 'LOAF \'N JUG', 'OWENS', 'QUIK STOP',
        'SHELL COMPANY', 'THE LITTLE CLINIC', 'TOM', 'TURKEY',
        'TURKEY HILL', 'TURKEY HILL MINIT MARKETS', 'VITACOST')]
    return chains_list


def get_locations(token: str, zip: int, chain: str, limit: int, radius: int):
    headers = {
        'Accept': 'application/json\\',
        'Authorization': 'Bearer ' + token,
    }
    params = {
        'filter.zipCode.near': zip,
        'filter.chain': chain,
        'filter.limit': limit,
        'filter.radiusInMiles': radius,
    }
    return requests.get('https://api.kroger.com/v1/locations',
                        params=params, headers=headers).json()