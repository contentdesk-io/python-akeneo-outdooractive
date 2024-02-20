from os import getenv
from dotenv import find_dotenv, load_dotenv
from akeneo.akeneo import Akeneo
import xml.etree.ElementTree as ET
load_dotenv(find_dotenv())

CDN_ENDPOINT = getenv('CDN_ENDPOINT')
OUTDOORACTIVE_SOURCE = getenv('OUTDOORACTIVE_SOURCE')
OUTDOORACTIVE_OWNER = getenv('OUTDOORACTIVE_OWNER')

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

def transformSingle(product):
    # Root
    pois = ET.Element("pois")
    pois.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
    pois.attrib["xsi:schemaLocation"] = "http://www.outdooractive.com/api/schema/alp.interface alp.interface.pois.xsd"
    source = ET.SubElement(pois, "source")
    source.text = OUTDOORACTIVE_SOURCE
    owner = ET.SubElement(pois, "owner")
    owner.text = OUTDOORACTIVE_OWNER
    # Poi
    poi = ET.SubElement(pois, "poi")
    poi.attrib["id"] = product["identifier"]
    if product["enabled"]:
        poi.attrib["workflow"] = "online"
    else:
        poi.attrib["workflow"] = "offline"
    poi.attrib["lastmodified"] = product["updated"]

    poiOwner = ET.SubElement(poi, "owner")
    poiOwner.text = OUTDOORACTIVE_OWNER

    if "categories" in product:
        if len(product["categories"]) > 0:
            categories = ET.SubElement(poi, "categories")                                                 
            for category in product["categories"]:
                ET.SubElement(categories, "category").text = category
        
    point = ET.SubElement(poi, "point")
    point.text = product["values"]["latitude"][0]["data"]+" "+product["values"]["longitude"][0]["data"]

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
    
    attributes = ET.SubElement(poi, "attributes")
    if "starRating" in product["values"]:
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
    
    # Descriptions
    if "description" in product["values"]:
        descriptions = ET.SubElement(poi, "descriptions")
        for productDescription in product["values"]["description"]:
            description = ET.SubElement(descriptions, "description")
            prefix = productDescription["locale"].split("_")[0]
            description.attrib["lang"] = prefix
            description.text = productDescription["data"]
            # Name
            if "name" in product["values"]:
                for productName in product["values"]["name"]:
                    if productName["locale"] == productDescription["locale"]:
                        title = ET.SubElement(description, "title")
                        title.text = productName["data"]
            if "disambiguatingDescription" in product["values"]:
                for disambiguatingDescription in product["values"]["disambiguatingDescription"]:
                    if disambiguatingDescription["locale"] == productDescription["locale"]:
                        abstract = ET.SubElement(description, "abstract")
                        abstract.text = disambiguatingDescription["data"]

    # Images
    images = ET.SubElement(poi, "images")
    if "image" in product["values"]:
        image = ET.SubElement(images, "image")
        image.attrib["id"] = product["values"]['image'][0]["data"]
        image.attrib["src"] = CDN_ENDPOINT+product["values"]['image'][0]["data"]
        point2 = ET.SubElement(image, "point")
        point2.text = point.text
        source2 = ET.SubElement(image, "source")
        source2.text = source.text

    #tree = ET.ElementTree(pois)
    #tree.write("output.xml")
    
    xml_string = ET.tostring(pois, encoding="utf-8", method="xml")
    xml_string = b'<?xml version="1.0" encoding="UTF-8"?>' + xml_string

    return xml_string.decode("utf-8")
