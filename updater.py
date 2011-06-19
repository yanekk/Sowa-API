from sowa.connector import SowaConnector
from sowa.requests.document import *
from sowa.requests.report import *
from marc.base import *

SowaConnector.connect("127.0.0.1", 42610)
rec = SowaUpdateTimeRequest()
iso_record = SowaIsoRequest(rec.rec_id()).result()
record = IsoRecord(iso_record, "cp1250")
