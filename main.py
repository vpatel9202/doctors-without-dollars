import requests
from requests.exceptions import HTTPError


# ---------------------------------------------------------------------------- #
#                               Common Variables                               #
# ---------------------------------------------------------------------------- #

nrmp_ein  = 362249886
nbme_ein  = 231352238
nbome_ein = 364135679
aamc_ein  = 362169124
ama_ein   = 360727175

propublica_api = 'https://projects.propublica.org/nonprofits/api/v2'


# ---------------------------------------------------------------------------- #
#                               Request Functions                              #
# ---------------------------------------------------------------------------- #

# Test for an HTTP response and if not "200", throw error.
def test_for_http_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

    except HTTPError as http_error:
        print(f'HTTP Error: {http_error}')
    except Exception as error:
        print(f'Non-HTTP error: {error}')
    else:
        print('Succesful HTTP response: {response}')
        return response
