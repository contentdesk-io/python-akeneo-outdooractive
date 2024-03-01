
import outdooractive
import json
# All Outdooractive POI categories
# https://www.outdooractive.com/api/project/api-dev-oa/category/tree/poi?key=yourtest-outdoora-ctiveapi&lang=de

# Get all Options for Outdooractive Attribut
# https://api.akeneo.com/api-reference.html#get_attributes__attribute_code__options
# /api/rest/v1/attributes/{attribute_code}/options
# outdooractive_poi_category


def __main__():
   print("STARTING")
   print("EXTRACTING")
   outdooractiveCategories =  outdooractive.getPOICategories()
   
   print("TRANSFORMING")
   # Save to JSON file Options
   #options = outdooractive.transformOptions(outdooractiveCategories)
   # Save to JSON file Categories
   # Save in Custom JSON Content-type 'application/vnd.akeneo.collection+json' with multiple lines   
   #with open('../examples/options.json', 'w') as file:
   #     json.dump(options, file)

   print("LOADING")
   # Upload per Option
   load = outdooractive.loadAttributOption(outdooractiveCategories, "outdooractive_poi_category")
   # One Upload with multiple lines
   #load = outdooractive.loadAttributOptions(outdooractiveCategories, "outdooractive_poi_category")
   print("DONE")

if __name__== "__main__":
    __main__()