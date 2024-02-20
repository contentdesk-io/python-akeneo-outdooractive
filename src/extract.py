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

def extract():
  data = getAkeneoProducts()
  return data