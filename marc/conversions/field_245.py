import re
from marc import IsoField

def removeSlashes(string):
    return string.strip(" /")

def setWarehouseInformation(field):
    s_f = field.subfield("b", True)
    if s_f:
        data = s_f.data.strip()
        matches = re.match("^\[(Magazyn.*?)\]$", data)
        if matches:
            field.remove_subfield(s_f)
            title = field.subfield("a", True)
            title.data = title.data.strip(":= ")
            return
        m = "^.*?(:|=){,1} \[Magazyn.*?\]\.{,1}$"
        matches = re.match(m, data)
        if matches:
            s_f.data = re.sub("\[Magazyn.*?\]\.{,1}", "", data).strip(": ")
#TODO: poprawic!

def findMovieGenre(record):
    title = record.field("245", True)
    subfield_b = title.subfield("b", True)
    if subfield_b:
        data = subfield_b.data.strip()
        match = re.match("^.*?\[ *?(Film.*?)(?:;|:) (DVD|VHS) *?\]", data)
        if match:
            if match.group(1).strip() != "Film":
                f = IsoField("655")
                f.ind_1 = "0"
                f.ind_2 = "4"
                f.add_subfield("a", match.group(1).strip())
                record.add_field(f)
            subfield_b.data = re.sub("\[Film.*?; (DVD|VHS)\]", "", subfield_b.data).strip(".")

            if subfield_b.data == "":
                title.remove_subfield(subfield_b)
                title.subfield("a", True).data = title.subfield("a", True).data.strip(":= ")
            else:
                subfield_b.data = subfield_b.data.strip(":= ")

#TODO: Poprawic!
from conversions.field_007 import IsoMaterial
def separateAudiobooks(record):
    title = record.field("245", True)
    subfield_b = title.subfield("b", True)
    if subfield_b:
        pattern = "\[Audio[\- ]*książk(a|i).*?\]"
        if re.match(pattern, subfield_b.data.strip(), re.IGNORECASE):
            re.sub(pattern, "", subfield_b.data.strip())
            if subfield_b.data.strip():
                title.remove_subfield(subfield_b)
                title.subfield("a", True).data = title.subfield("a", True).data.strip(" :")
                for field in record.field("949"):
                    field.subfield("t", True).data = "KM "
            else:
                subfield_b.data.strip(" :")

