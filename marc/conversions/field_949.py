"""
V    : magazyn bd64
C    : czytelnia naukowa nr XIX
D    : wypożyczalnia dla dzieci 117
E    : czytelnia w117
F    : magazyn bd64
K    : czytelnia (bd64)
M    : magazyn czytelni nr XIX
N    : wypożyczalnia 117
O    : wypożyczalnia dla dzieci 129
S    : wypożyczalnia 129
T    : biblioteka dla dzieci 64
W    : wypożyczalnia 116


1   : Wypożyczalnia 116
 2   : Wypożyczalnia 117 - dorośli
 3   : Czytelnia Naukowa Nr XIX
 4   : Biblioteka dziecięca BD 64
 5   : Wypożyczalnia 117 - dzieci
 6   : Wypożyczalnia 129
 7   : Wypożyczalnia 129 - dzieci
"""


def setLocation(field):
    location_tags = {
        "V" : 4,
        "C" : 3,
        "D" : 5,
        "E" : 2,
        "F" : 4,
        "K" : 4,
        "M" : 3,
        "N" : 2,
        "O" : 7,
        "S" : 6,
        "T" : 4,
        "W" : 1
    }
    locations = {
        1   : "Wypożyczalnia 116",
        2   : "Wypożyczalnia 117 - dorośli",
        3   : "Czytelnia Naukowa Nr XIX",
        4   : "Biblioteka dziecięca BD 64",
        5   : "Wypożyczalnia 117 - dzieci",
        6   : "Wypożyczalnia 129",
        7   : "Wypożyczalnia 129 - dzieci"
    }
    for subfield in field.subfield("h"):
        field.add_subfield("l", locations[location_tags[subfield.data.strip()]])

