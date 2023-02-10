import requests


def get_products(token: str,
                 searchterm: str,
                 locID: str = '01400513',
                 limit: int = 10,
                 ) -> dict:
    '''Return a dictionary of products from a search.

    Retrieves products for a search term and returns the JSON-formatted result 
    as a dictionary.

    Args:
        token: A string from get_token().
        searchterm: A user-provided string to search.
        locID: A string that can be user-provided or from get_locations().
        limit: A user-provided integer of the desired number of results.

    Returns:
        A dictionary containing JSON data of product information from search
        results.
    '''

    headers = {
        'Accept': 'application/json\\',
        'Authorization': 'Bearer ' + token,
    }
    params = {
        'filter.term': searchterm,
        'filter.locationId': locID,
        'filter.fulfillment': 'ais',
        'filter.limit': limit,
    }
    response = requests.get('https://api.kroger.com/v1/products',
                            params=params, headers=headers)
    if response.ok:
        product_data = response.json()
    else:
        product_data = []
    return product_data


def get_products_by_id(token: str,
                 locID: str = '01400513',
                 productID: str = '',
                 ) -> dict:
    '''Return a dictionary of products from a search.

    Retrieves data for a/some product id(s) and returns the JSON-formatted 
    result as a dictionary.

    Args:
        token: A string from get_token().
        locID: A string that can be user-provided or from get_locations().
        productID: A string that can be user-provided or from upcs.txt. May be
          one product id or multiple, comma-separated.


    Returns:
        A dictionary containing JSON data of product information from search
        results.
    '''

    headers = {
        'Accept': 'application/json\\',
        'Authorization': 'Bearer ' + token,
    }

    params = {
    "filter.locationId": locID,
    "filter.productId": productID,
    "filter.fulfillment": "ais",
    }

    

    response = requests.get("https://api.kroger.com/v1/products",
                        params=params, headers=headers)
    if response.ok:
        product_data = response.json()
    else:
        product_data = []
    return product_data