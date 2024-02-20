import json
from dicttoxml import dicttoxml

# Transform data to XML
def transform(data):
     # Transform data to XML
    print("Transforming data to XML")

    # JSON als String
    json_string = '{"name": "John", "age": 30, "city": "New York"}'

    # JSON in ein Python-Dict umwandeln
    json_dict = json.loads(json_string)
   
    xml = dicttoxml(json_dict)
    print(xml)
    return xml

