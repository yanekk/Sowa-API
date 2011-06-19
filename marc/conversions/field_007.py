
"""C    : czasopismo
    00   : nieregularne
    01   : rocznik
    02   : półrocznik
    04   : kwartalnik
    06   : dwumiesięcznik
    12   : miesięcznik
    26   : dwutygodnik
    52   : tygodnik
    99   : dziennik
D    : dzieło wielotomowe
K    : zbiory specjalne
    C    : elektroniczne
    M    : audio-ksišżka
    V    : audiowizualne
N    : numery czasopisma
    R    : rocznik
    Z    : zeszyt
S    : seria wydawnicza
         : seria wydawnicza
    C    : cykl autorski
T    : tom lub częć
D    : literatura dla dorosłych
    N    : literatura popularno-naukowa
    O    : literatura obcojęzyczna
    P    : literatura piękna dla dzieci
Y    : prace współwydane
Z    : dzieło jednotomowe
    D    : literatura dla dorosłych
    I    : inf.bibliograficzna
    N    : literatura popularno-naukowa
    O    : literatura obcojęzyczna
    P    : literatura piękna dla dzieci
"""
from marc import IsoField
class IsoMaterial:
    AUDIO_BOOK = "sd"
    DVD_MOVIE  = "vd"
    ELECTRONIC = "co"
    def get_k(self, second):
        if second == "m":
            return IsoMaterial.AUDIO_BOOK
        if second == "v":
            return IsoMaterial.DVD_MOVIE
        return IsoMaterial.ELECTRONIC

    @classmethod
    def setMaterial(cls, record):
        material = IsoMaterial()

        for field in record.field("949"):
            for subfield in field.subfield("t"):
                data = subfield.data.strip().lower()
                method = "get_{0}".format(data[0]).lower()

                if hasattr(material, method):
                    method = getattr(material, method)
                    result = method(data[1])
                    if result:
                        record.add_field(IsoField("007", result))

