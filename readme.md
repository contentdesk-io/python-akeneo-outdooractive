
# Export
## Singel Export / singleExport.py
Einzelnes Objekt das exportiert wird.

## Full Export / fullExport.py
Alle Objekte die eine Outdooractive Kategorie haben

# ETL-Process

## Extract
Extrahiert alle Objekte mit einer Outdooractive Kategorie, welche Vollständig und aktiv sind.

## Transform
Wandelt alle Akeneo Objekte in Outdooractive XML-Fomate / Termology gemäss Outdooracitve Interface Schnittstelle um.

## Load
Ladet alle XML eines Objekt in einen S3 Storage hoch und
stosst den Import bei Outdooractive an.