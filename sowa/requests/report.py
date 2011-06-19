from sowa.requests.base import SowaRequest
from sowa.static import *

class SowaReportRequest(SowaRequest):
   def __init__(self, rec_id, report_id):
      self.request_type = REPORT_REQUEST
      SowaRequest.__init__(self, 100, "\x02", report_id, rec_id, "\x00")

class SowaIsoRequest(SowaReportRequest):
   def __init__(self, rec_id):
      SowaReportRequest.__init__(self, rec_id, 4)
