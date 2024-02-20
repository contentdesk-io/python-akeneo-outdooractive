from os import getenv
from dotenv import find_dotenv, load_dotenv
from akeneo.akeneo import Akeneo
import xml.etree.ElementTree as ET
load_dotenv(find_dotenv())

CDN_ENDPOINT = getenv('CDN_ENDPOINT')
OUTDOORACTIVE_SOURCE = getenv('OUTDOORACTIVE_SOURCE')
OUTDOORACTIVE_OWNER = getenv('OUTDOORACTIVE_OWNER')
OUTDOORACTIVE_OWNERNAME = getenv('OUTDOORACTIVE_OWNERNAME')

# Transform data to XML
def transform(products):
    # Root
    pois = ET.Element("pois")
    pois.attrib["xsi:schemaLocation"] = "http://www.outdooractive.com/api/schema/alp.interface alp.interface.pois.xsd"
    source = ET.SubElement(pois, "source")
    source.text = "tso-test"
    owner = ET.SubElement(pois, "owner")
    owner.text = "pim-test"
    # Poi
    for product in products:
        poi = ET.SubElement(pois, "poi")
        poi.attrib["id"] = product["identifier"]
        poi.attrib["workflow"] = "online"
        poi.attrib["lastmodified"] = "2021-01-01T00:00:00"
        for key, value in product.items():
            ET.SubElement(poi, key).text = value
    return pois

def coordinates(product):
    point = ET.Element("point")
    point.text = product["values"]["latitude"][0]["data"]+" "+product["values"]["longitude"][0]["data"]
    return point

def setImage(product, point=None):
    image = ET.Element("image")
    image.attrib["id"] = product["data"].split("/")[4].split(".")[0]
    image.attrib["src"] = CDN_ENDPOINT+product["data"]
    image.append(point)
    source = ET.SubElement(image, "source")
    source.text = OUTDOORACTIVE_OWNERNAME
    return image

def addImage(product, scope=None, point=None):
    image = ET.Element("image")
    if scope is None:
        image = setImage(product[0], point)
    else:
        for productRow in product:
            if productRow["scope"] == scope:
                image = setImage(productRow, point)
    return image

def transformSingle(product):
    # Root
    # pois = ET.Element("pois")
    # pois.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
    # pois.attrib["xsi:schemaLocation"] = "http://www.outdooractive.com/api/schema/alp.interface alp.interface.pois.xsd"
    # source = ET.SubElement(pois, "source")
    # source.text = OUTDOORACTIVE_SOURCE
    # owner = ET.SubElement(pois, "owner")
    # owner.text = OUTDOORACTIVE_OWNER
    # Poi
    poi = ET.Element("poi")
    poi.attrib["id"] = product["identifier"]
    if product["enabled"]:
        poi.attrib["workflow"] = "online"
    else:
        poi.attrib["workflow"] = "offline"
    poi.attrib["lastmodified"] = product["updated"]

    poiOwner = ET.SubElement(poi, "owner")
    poiOwner.text = OUTDOORACTIVE_OWNER

    if "outdooractive_poi_category" in product['values']:
        categories = ET.SubElement(poi, "categories")
        ET.SubElement(categories, "category").text = product["values"]["outdooractive_poi_category"][0]["data"]

    point = coordinates(product)
    poi.append(point)

    contact = ET.SubElement(poi, "contact")
    address = ET.SubElement(contact, "address")
    if "streetAddress" in product["values"]:
        street = ET.SubElement(address, "street")
        street.text = product["values"]["streetAddress"][0]["data"]
    if "addressLocality" in product["values"]:
        municipality = ET.SubElement(address, "municipality")
        municipality.text = product["values"]["addressLocality"][0]["data"]
    if "postalCode" in product["values"]:
        postalCode = ET.SubElement(address, "postalcode")
        postalCode.text = product["values"]["postalCode"][0]["data"]
    # Has scope
    if "telephone" in product["values"]:
        tel = ET.SubElement(contact, "tel")
        tel.text = product["values"]["telephone"][0]["data"]
    if "email" in product["values"]:
        email = ET.SubElement(contact, "email")
        email.text = product["values"]["email"][0]["data"]
    if "website" in product["values"]:
        url = ET.SubElement(contact, "url")
        url.text = product["values"]["website"][0]["data"]
    
    if "starRating" in product["values"]:
        attributes = ET.SubElement(poi, "attributes")
        hotelstars = ET.SubElement(attributes, "hotelstars")
        if product["values"]["starRating"][0]["data"] == "1":
            hotelstars.text = "1"
        elif product["values"]["starRating"][0]["data"] == "2":
            hotelstars.text = "2"
        elif product["values"]["starRating"][0]["data"] == "3":
            hotelstars.text = "3"
        elif product["values"]["starRating"][0]["data"] == "4":
            hotelstars.text = "4"
        elif product["values"]["starRating"][0]["data"] == "5":
            hotelstars.text = "5"
        if "accommodation_classification_superior" in product["values"]:
             hotelstars.text =  str(hotelstars.text) + str(".5")
    
    # Name
    if "name" in product["values"]:
        descriptions = ET.SubElement(poi, "descriptions")
        for productName in product["values"]["name"]:
            description = ET.SubElement(descriptions, "description")
            prefix = productName["locale"].split("_")[0]
            description.attrib["lang"] = prefix
            title = ET.SubElement(description, "title")
            title.text = productName["data"]
            # Descriptions
            if "description" in product["values"]:
                for productDescription in product["values"]["description"]:
                    if productDescription["locale"] == productName["locale"]:
                        description.text = productDescription["data"]
            # DisambiguatingDescription
            if "disambiguatingDescription" in product["values"]:
                for disambiguatingDescription in product["values"]["disambiguatingDescription"]:
                    if disambiguatingDescription["locale"] == productDescription["locale"]:
                        abstract = ET.SubElement(description, "abstract")
                        abstract.text = disambiguatingDescription["data"]

    # Images
    images = ET.SubElement(poi, "images")
    if "image" in product["values"]:
        image = addImage(product["values"]['image'], None, point)
        images.append(image)

    if "image_01_scope" in product["values"]:
        image01 = addImage(product["values"]['image_01_scope'], "ecommerce", point)
        images.append(image01)
    
    if "image_02_scope" in product["values"]:
        image02 = addImage(product["values"]['image_02_scope'], "ecommerce", point)
        images.append(image02)

    if "image_03_scope" in product["values"]:
        image03 = addImage(product["values"]['image_03_scope'], "ecommerce", point)
        images.append(image03)
    
    if "image_04_scope" in product["values"]:
        image04 = addImage(product["values"]['image_04_scope'], "ecommerce", point)
        images.append(image04)
    
    if "image_05_scope" in product["values"]:
        image05 = addImage(product["values"]['image_05_scope'], "ecommerce", point)
        images.append(image05)
    
    if "image_06_scope" in product["values"]:
        image06 = addImage(product["values"]['image_06_scope'], "ecommerce", point)
        images.append(image06)
    
    if "image_07_scope" in product["values"]:
        image07 = addImage(product["values"]['image_07_scope'], "ecommerce", point)
        images.append(image07)
    
    if "image_08_scope" in product["values"]:
        image08 = addImage(product["values"]['image_08_scope'], "ecommerce", point)
        images.append(image08)

    if "image_09_scope" in product["values"]:
        image09 = addImage(product["values"]['image_09_scope'], "ecommerce", point)
        images.append(image09)
    
    if "image_10_scope" in product["values"]:
        image10 = addImage(product["values"]['image_10_scope'], "ecommerce", point)
        images.append(image10)
    
    xml_string = ET.tostring(poi, encoding="utf-8", method="xml")
    #xml_string = b'<?xml version="1.0" encoding="UTF-8"?>' + xml_string

    return xml_string.decode("utf-8")