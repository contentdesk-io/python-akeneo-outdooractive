from extract import getAkeneoProduct
from transform import transform
from load import loadProduct
import sys

if len(sys.argv) > 1:
    identifier = sys.argv[1]
    print(identifier)
else:
    identifier = 'c0d07da1-7875-4053-b129-2820385dade7'

def __main__():
   print("STARTING")
   print("EXTRACTING")
   extractData = getAkeneoProduct(identifier)
   
   print("TRANSFORMING")
   #transformData = transform(extractData) 

   print("LOADING")
   loadData = loadProduct(extractData)
   print("DONE")

if __name__== "__main__":
    __main__()