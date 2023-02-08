import requests


def get_chains(token: str) -> list:
    '''Return a list of shoppable subsidiaries of the Kroger Company.

    Retrieves the current list of chains operated by Kroger, then filters out 
    names of chains without significant shoppability (pharmacies, clinics, 
    fuel stations, etc).

    Args:
        token: A string from get_token().

    Returns:
        A list of shoppable and searchable grocery chains.
    '''

    heads = {
        'Accept': 'application/json\\',
        'Authorization': 'Bearer ' + token,
    }
    chains_data = requests.get('https://api.kroger.com/v1/chains',
                               headers=heads)
    chains_list = []
    if chains_data.ok:
        chains_json = chains_data.json()
        for i in range(len(chains_json.get('data'))):
            chains_list.append(chains_json.get('data')[i].get('name'))
        chains_list = [e for e in chains_list if e not in (
            'AMOCO', 'BP', 'COPPS', 'COVID', 'EG GROUP', 'FRED',
            'FRESH EATS MKT', 'HARRIS TEETER FUEL',
            'HARRIS TEETER FUEL CENTER', 'HART', 'JEWELRY', 'KWIK',
            'KWIK SHOP', 'LOAF', 'LOAF \'N JUG', 'OWENS', 'QUIK STOP',
            'SHELL COMPANY', 'THE LITTLE CLINIC', 'TOM', 'TURKEY',
            'TURKEY HILL', 'TURKEY HILL MINIT MARKETS', 'VITACOST')]
    else:
        pass
    return chains_list


def get_locations(token: str,
                  zip: int = 45202,
                  chain: str = 'KROGER',
                  limit: int = 10,
                  radius: int = 25
                  )-> dict:
    '''Return a dictionary of locations near a ZIP code.

    Retrieves store locations for a particular chain within a radius of a ZIP
    code and returns the JSON-formatted result as a dictionary.

    Args:
        token: A string from get_token().
        zip: A user-provided integer Zip code.
        chain: A string that can be user-provided or from get_chains().
        limit: A user-provided integer of the desired number of results.
        radius: A user-provided integer of the search distance in miles.

    Returns:
        A dictionary containing JSON data for store locations within the
        provided boundaries.
    '''

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
    response = requests.get('https://api.kroger.com/v1/locations',
                        params=params, headers=headers)
    if response.ok:
        location_data = response.json()
    else:
        location_data = []
    return location_data
