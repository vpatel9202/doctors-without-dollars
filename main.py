import requests
from requests.exceptions import HTTPError
import json


# ---------------------------------------------------------------------------- #
#                               Common Variables                               #
# ---------------------------------------------------------------------------- #

nrmp_ein  = 362249886
nbme_ein  = 231352238
nbome_ein = 364135679
aamc_ein  = 362169124
ama_ein   = 360727175

pp_search_url = 'https://projects.propublica.org/nonprofits/api/v2/search.json'
pp_org_url = 'https://projects.propublica.org/nonprofits/api/v2/organizations/{}.json'


# ---------------------------------------------------------------------------- #
#                               Request Functions                              #
# ---------------------------------------------------------------------------- #

# Test for an HTTP response and if not "200", throw error.
def get_http_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

    except HTTPError as http_error:
        print(f'HTTP Error: {http_error}')
    except Exception as error:
        print(f'Non-HTTP error: {error}')
    else:
        print(f'Succesful HTTP response: {response}')
        return response

# Get organization data as JSON
def get_org_data_as_json(ein):
    url = pp_org_url.format(ein)

    response = get_http_response(url).json()
    return response
