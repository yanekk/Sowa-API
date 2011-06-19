from collections import OrderedDict
from io import StringIO

F_T = "\x1e"
F_S = "\x1f"
R_S = "\x1d"

class IsoLeader(object):

    def __init__(self, leader_data):

        self.data = OrderedDict()
        self.data["length"]              = leader_data[0:5]
        self.data["record_status"]       = leader_data[5]
        self.data["record_type"]         = leader_data[6]
        self.data["bibliographic_level"] = leader_data[7]
        self.data["type_of_control"]     = leader_data[8]
        self.data["coding_scheme"]       = leader_data[9]
        self.data["indicator_count"]     = leader_data[10]
        self.data["subfield_code_count"] = leader_data[11]
        self.data['base_address']        = leader_data[12:17]
        self.data["rest"]                = leader_data[17:]

    def render(self):
        data = ""
        for key in self.data:
            data += self.data[key]
        return data

    def get_data(self, key):
        return self.data[key]

    def set_data(self, key, value):
        self.data[key] = value

    def set_length(self, value):
        self.set_data("length", str(value+24).rjust(5, "0"))

    def get_length(self):
        return int(self.get_data("length"))

    def set_base_address(self, value):

        self.set_data("base_address", str(value+25).rjust(5, "0"))

    def __str__(self):
        return self.render()

class IsoSubField(object):
    def __init__(self, code, data):
        self.data = data
        self.code = code

    def set_data(self, data):
        self.data = data

    def to_iso(self):
        return F_S+self.code+self.data

    def __str__(self):
        return "{0}({1})".format(self.code, self.data)
        pass

class IsoField(object):
    def __init__(self, tag, field_data=None):
        self.tag = tag
        self.subfields = OrderedDict()
        self.data = None
        if field_data:
            if self.tag[0:2] == "00":
                self.data = field_data
                return
            else:
                self.ind_1 = field_data[0]
                self.ind_2 = field_data[1]

                [self.add_subfield(i[0], IsoSubField(i[0], i[1:])) for i in field_data[3:].split(F_S)]

    def add_subfield(self, code, data):
        if isinstance(data, str):
            data = IsoSubField(code, data)

        if not code in self.subfields:
            self.subfields[code] = []
        self.subfields[code].append(data)

    def remove_subfield(self, subfield):
        for s_f in self.subfields[subfield.code]:
            if s_f == subfield:
                self.subfields[subfield.code].remove(s_f)

    def subfield(self, code, single = False):
        if code is list:
            code = [code]
        l = []
        for code in code:
            try:
                data = self.subfields[code]
                l.append('')
                l[-1:] = data
            except KeyError:
#                print ("code {0} not found in {1}".format(code, self.to_iso()))
                pass
        if single and len(l):
            return l[0]
        elif single:
            return None
        return l

    def all_subfields(self):
        c = []
        for key in self.subfields:
            data = self.subfields[key]
            for i in data:
                c.append(i)
        return c

    def __str__(self):
        all_subfields = self.all_subfields()
        if not len(all_subfields):
            return self.tag+" "+self.data
        else:
            return self.tag+" 1({0}) 2({1}) ".format(self.ind_1, self.ind_2)+", ".join([str(i) for i in all_subfields])

    def to_iso(self):
        all_subfields = self.all_subfields()
        iso = ""
        iso += F_T
        if not len(all_subfields):
            iso += self.data
            data = self.data
        else:
            iso += self.ind_1
            iso += self.ind_2
            data = "".join([i.to_iso() for i in all_subfields])

            iso += data

        length = len(iso.encode("utf-8"))
        return [self.tag, length, iso]

ENCODING = "cp1250"

class NoFieldError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        pass

class EndOfFile(Exception):
    def __init__(self):
        pass



class IsoRecord(object):
    def __init__(self, iso_file, encoding):
        iso_file = StringIO(iso_file)
        self.leader = IsoLeader(iso_file.read(24))
        self.load_directory(iso_file)
        self.load_fields(iso_file)

    def load_directory(self, iso_file):
        self.directory = []
        marker = iso_file.read(1)
        fields = []
        while True:
            if marker == "":
                raise EndOfFile()
            if marker == F_T:
                break
            self.directory.append(((marker+iso_file.read(2)), iso_file.read(4), iso_file.read(5)))
            marker = iso_file.read(1)

    def load_fields(self, iso_file):
        self.fields = OrderedDict()
        for i in self.directory:
            self.add_field(IsoField(i[0], iso_file.read(int(i[1])).strip(F_T)))

    def remove_field(self, field):
        for f in self.fields[field.tag]:
            if f == field:
                self.fields[field.tag].remove(f)

    def add_field(self, field):
        if not field.tag in self.fields:
            self.fields[field.tag] = []
        self.fields[field.tag].append(field)

    def field(self, tag, single=False):
        try:
            data = self.fields[tag]
        except KeyError:
            raise NoFieldError(tag)
        if single:
            return data[0]
        return data

    def all_fields(self):
        c = []
        sorted_tags = sorted(self.fields)
        for tag in sorted_tags:
            data = self.fields[tag]
            c.append('')
            c[-1:] = data
        return c

    def each_subfield(self, field_tag, subfield_code, callback):
        for field in self.field(field_tag):
            for subfield in field.subfield(subfield_code):
                subfield.data = callback(subfield.data)

    def each_field(self, field_tag, callback):
        for field in self.field(field_tag):
            callback(field)

    def __str__(self):
        return str(self.leader)+"\n"+"\n".join([str(i) for i in self.all_fields()])

    def to_iso(self):
        iso    = ""
        marker = 0
        fields = [field.to_iso() for field in self.all_fields()]

        fields_iso = ""
        for field in fields:
            iso += field[0]
            iso += str(field[1]).rjust(4, "0")
            iso += str(marker).rjust(5, "0")
            fields_iso += field[2]
            marker += field[1]

        self.leader.set_base_address(len(iso))
        iso += fields_iso
        iso += F_T
        self.leader.set_data("coding_scheme", "a")
        self.leader.set_length(len(iso.encode("utf-8")))

        iso = self.leader.render()+iso
        return (iso+R_S).encode("utf-8")

class IsoCollection(object):
    def __init__(self):
        pass

    def next(self):
        content = ""
        while True:
            marker = self.iso_file.read(1)
            if marker == "":
                return None
            if(marker == R_S):
                return IsoRecord(content, self.encoding)

            content += marker
        return None

    def feed_with_file(self, file, encoding = ENCODING):
        self.encoding = encoding
        self.iso_file = open(file, "r", encoding=encoding)

