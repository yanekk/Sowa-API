"""
from sowa.requests.document import *
from marc.base import *

rec = SowaUpdateTimeRequest()
iso_record = SowaIsoRequest(rec.rec_id()).result()
record = IsoRecord(iso_record, "cp1250")
"""

from log_analyzer.base import LogAnalyzer
from log_analyzer.rules import *
from log_analyzer.timer import LogAnalyzerTimer
from service.update import ServiceUpdater
from sowa.connector import SowaConnector
SowaConnector.connect("127.0.0.1", 42610)

f = ServiceUpdater("http://urlblabla.com/", "<api_key")
l = LogAnalyzer("../log/warszawa_ursus_ks.log", LogAnalyzerTimer("2011-06-20"))
l.add_rule(SowaDeleteRule(f))
l.add_rule(SowaModificationRule(f))
l.analyze()

if f.update():
   l.rename()
else:
   print(f.error_message())
   l.close()