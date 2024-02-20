import json
from dicttoxml import dicttoxml

import xml.etree.ElementTree as ET

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
    pois.attrib["xsi:schemaLocation"] = "http://www.outdooractive.com/api/schema/alp.interface alp.interface.pois.xsd"
    source = ET.SubElement(pois, "source")
    source.text = "tso-test"
    owner = ET.SubElement(pois, "owner")
    owner.text = "pim-test"
    # Poi
    poi = ET.SubElement(pois, "poi")
    poi.attrib["id"] = product["identifier"]
    poi.attrib["workflow"] = "online"
    poi.attrib["lastmodified"] = "2021-01-01T00:00:00"

    poiOwner = ET.SubElement(poi, "owner")
    poiOwner.text = "pim-test"

    #tree = ET.ElementTree(pois)
    #tree.write("output.xml")
    xml_string = ET.tostring(pois, encoding="utf-8", method="xml")

    return xml_string.decode("utf-8")
