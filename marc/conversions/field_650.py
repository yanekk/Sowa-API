"""
do 1795 r.
"""
from marc import NoFieldError
import re, sys
def setEra(field):
    matches = ["(od |do ){,1}[0-9\-]+ w(\.|iek){,1}",
               "(od |do ){,1}[0-9]{3,4}( {,1}\-[0-9]{3,4}){,1}( ){,1}(r\.{,1}){,1}",
               "(od |do ){,1}[xiv]+( {,1}|\-[xiv]+ ){,1}w(\.|iek){,1}",
               "(od |do ){,1}[0-9]+(\-[0-9]+)* w\.p\.n\.e\."
              ]

    for subfield in field.subfield("x"):
        m = False
        for match in matches:
            if re.match("^{0}$".format(match), subfield.data.strip(), re.IGNORECASE):
                m = True

        if m:
            subfield.data = subfield.data.strip()
            subfield.code = "y"

def findGenres(record):
    fields_for_change = []
    try:
        for field in record.field("650"):
            genre_headers_pattern = "^(Powieść|Opowiadanie|Literatura dziecięca|Słownik|Encyklopedi(a|e)|Atlas|Audioksiążka|Bajka i baśń|Literatura młodzieżowa|Poezja polska|Publicystyka polska|Literatura polska|Pamiętniki).*$"
            topic = field.subfield("a", True).data.strip()
            if re.match(genre_headers_pattern, topic):
                fields_for_change.append(field)

        for field in fields_for_change:
            record.remove_field(field)
            field.tag = "655"
            record.add_field(field)
    except NoFieldError:
        pass

