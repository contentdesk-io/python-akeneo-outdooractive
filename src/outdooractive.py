# All Outdooractive POI categories
# https://www.outdooractive.com/api/project/api-dev-oa/category/tree/poi?key=yourtest-outdoora-ctiveapi&lang=de

import requests
from os import getenv
from dotenv import find_dotenv, load_dotenv
from akeneo.akeneo import Akeneo
import requests
load_dotenv(find_dotenv())

AKENEO_HOST = getenv('AKENEO_HOST')
AKENEO_CLIENT_ID = getenv('AKENEO_CLIENT_ID')
AKENEO_CLIENT_SECRET = getenv('AKENEO_CLIENT_SECRET')
AKENEO_USERNAME = getenv('AKENEO_USERNAME')
AKENEO_PASSWORD = getenv('AKENEO_PASSWORD')

def getAkeneoProducts():
  akeneo = Akeneo(
    AKENEO_HOST,
    AKENEO_CLIENT_ID,
    AKENEO_CLIENT_SECRET,
    AKENEO_USERNAME,
    AKENEO_PASSWORD
  )
  searchQuery = '{"enabled":[{"operator":"=","value":true}],"completeness":[{"operator":"=","value":100}],"outdooractive_poi_category":[{"operator":"NOT EMPTY"}]}&search_scope=ecommerce'
  return akeneo.getProducts(limit=100, search=searchQuery )

def getAkeneoProduct(identifier):
  akeneo = Akeneo(
    AKENEO_HOST,
    AKENEO_CLIENT_ID,
    AKENEO_CLIENT_SECRET,
    AKENEO_USERNAME,
    AKENEO_PASSWORD
  )
  return akeneo.getProductByCode(identifier)

def getPOICategories():
    url = "https://www.outdooractive.com/api/project/api-dev-oa/category/tree/poi?key=yourtest-outdoora-ctiveapi&lang=de"

    response = requests.get(url, headers={"Accept": "application/json"})

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}")
    else:
        data = response.json()
        print("Data fetched successfully")
    return data

def transformOptions(outdooractiveCategories):
    # create json with multiple lines for each option
    updateOptions = []
    for key, value in outdooractiveCategories.items():
        if key == "category":
            for category in value:
                for optionkey, optionvalue in category.items():
                    if optionkey == "category":
                        for option in optionvalue:
                            print(option['datatype'][0])
                            print(option['name'])
                            attributeOptionCode = option["datatype"][0]
                            body = {
                               "code": attributeOptionCode,
                               "attribute": "outdooractive_poi_category",
                               "labels": {
                                   "de_DE": option["name"]
                                }
                            }
                            updateOptions.append(body)
    return updateOptions

def loadAttributOption(outdooractiveCategories, attribut):
    akeneo = Akeneo(
        AKENEO_HOST,
        AKENEO_CLIENT_ID,
        AKENEO_CLIENT_SECRET,
        AKENEO_USERNAME,
        AKENEO_PASSWORD
    )

    for key, value in outdooractiveCategories.items():
        if key == "category":
            for category in value:
                #print(category['datatype'][0])
                for optionkey, optionvalue in category.items():
                    if optionkey == "category":
                        for option in optionvalue:
                            print(option['datatype'][0])
                            print(option['name'])
                            attributeOptionCode = option["datatype"][0]
                            body = {
                               "code": attributeOptionCode,
                               "attribute": attribut,
                               "labels": {
                                   "de_DE": option["name"]
                                }
                            }
                            response = akeneo.patchAttributOptionsByCode(attributeOptionCode, attribut, body)
                            print(response)
    print("FINSIHED - UPDATED ATTRIBUT OPTIONS") 

def loadAttributOptions(outdooractiveCategories, attribut):
    akeneo = Akeneo(
        AKENEO_HOST,
        AKENEO_CLIENT_ID,
        AKENEO_CLIENT_SECRET,
        AKENEO_USERNAME,
        AKENEO_PASSWORD
    )

    # create json with multiple lines for each option
    updateOptions = []
    for key, value in outdooractiveCategories.items():
        if key == "category":
            for category in value:
                for optionkey, optionvalue in category.items():
                    if optionkey == "category":
                        for option in optionvalue:
                            print(option['datatype'][0])
                            print(option['name'])
                            attributeOptionCode = option["datatype"][0]
                            body = {
                               "code": attributeOptionCode,
                               "attribute": attribut,
                               "labels": {
                                   "de_DE": option["name"]
                                }
                            }
                            updateOptions.append(body)

                            ##response = akeneo.patchAttributOptionsByCode(attributeOptionCode, attribut, body)
                            #print(response)

    response = akeneo.patchAttributOptions(attribut, updateOptions)
    print(response)
    print("FINSIHED - UPDATED ATTRIBUT OPTIONS") 

