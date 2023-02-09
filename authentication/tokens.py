import time

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

def get_token(client_id: str,
              client_secret: str
              ) -> list:
    '''Return a token when provided with client credentials.

    Retrieves a token from the API for future authentication needs.

    Args:
        client_id: A string that can be user-provided or from config file.
        client_secret: A string that can be user-provided or from config file.

    Returns:
        A list containing the authentication token and the time it expires.
    '''

    # Oauthlib client id, secret, and scope
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id,
                                        scope='product.compact')
    oauth = OAuth2Session(client=client, scope='product.compact')
    # Fetch token and derive token/expiration
    full_token = oauth.fetch_token(
        token_url='https://api.kroger.com/v1/connect/oauth2/token',
        auth=auth)
    if full_token.get('access_token'):
        token = full_token.get('access_token')
        # full_token.get('expires_at') will return the expiration time, but may be
        # deprecated, as the API reference no longer lists expires_at as a response.
        token_exp = time.time() + full_token.get('expires_in')
        return [token, token_exp]
    else:
        return []


def is_token_expiring(token: str,
                      token_exp: float,
                      client_id: str,
                      client_secret: str
                      ) -> list:
    '''Check and refresh token if needed.

    Retrieves a token from the API for future authentication needs.

    Args:
        token: A string from get_token().
        token-exp: A float from get_token().
        client_id: A string that can be user-provided or from config file.
        client_secret: A string that can be user-provided or from config file.

    Returns:
        A list containing the authentication token and the time it expires.
    '''

    if (float(token_exp) - time.time()) < 300:
        get_token(client_id, client_secret)
    else:
        return [token, token_exp]