import requests
from requests.exceptions import HTTPError
import json
import pandas
import xmltodict
from pathlib import Path
import xml.etree.ElementTree as ET
import re


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


# ----------------------------- API Interactions ----------------------------- #

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


# ----------------------------- File Manipulation ---------------------------- #

# Save JSON to a file
def save_json_to_file(write_data, write_file):
    with open(write_file, "w") as f:
        json.dump(write_data, f)

# Read JSON from file
def read_json_from_file(read_file):
    with open(read_file) as f:
        read_data = json.load(f)

    return read_data

# Read XML data and convert it to JSON data (optionally save it to JSON file)
def xml_to_json(xml_file, **kwargs):
    json_file = kwargs.get('json_file', None)

    with open(xml_file) as f:
        xml_dict = xmltodict.parse(f.read())
        xml_dict = xml_dict['Return']['ReturnData']

    if json_file:
        save_json_to_file(xml_dict, json_file)

    else:
        json_data = json.dumps(xml_dict)
        return json_data


# ----------------------------- Data Manipulation ---------------------------- #

# Clean pandas dataframes of whitespace cells with no other data
def clean_df(dataframe):
    df = dataframe.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    return df

# Read complete organization JSON file obtained from **PROPUBLICA API** and
# return filing data as pandas dataframe
def filing_data_from_org_json(filename, transpose=False):
    json_data = read_json_from_file(filename)
    filing_data = json_data['filings_with_data']
    columns = filing_data[0].keys()

    df = pandas.DataFrame(filing_data, columns=columns)
    df = df.set_index('tax_prd_yr')

    df = clean_df(df)

    if transpose is True:
        df = df.transpose()

    return df

# Create dataframe object from IRS XML files by first flattening them
def xml_to_df(filename, transpose=False):
    tree = ET.parse(filename)
    root = tree.getroot()

    parent_map = {}
    for p in tree.iter():
        for c in p:
            url_pattern = re.compile(r"{(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?}")
            tag_name = url_pattern.sub("", c.tag)
            parent_map[tag_name] = [c.text]

    df = pandas.DataFrame(parent_map)

    filing_year = [Path(filename).stem]
    df['filing_year'] = filing_year
    df.set_index('filing_year', inplace=True, drop=True)
    df.index = df.index.astype(int)

    df = clean_df(df)

    if transpose is True:
        df = df.transpose()

    return df

# Create dataframe with aggregated data from yearly XML filings from the IRS
def xml_dir_to_df(xml_dir, transpose=False):
    df = pandas.DataFrame()

    pathlist = Path(xml_dir).glob('*.xml')
    for path in pathlist:
        new_df = xml_to_df(path)
        df = pandas.concat([df, new_df], sort=False)

    df.sort_index(axis=0, inplace=True)

    df = clean_df(df)

    if transpose is True:
        df = df.transpose()

    return df
