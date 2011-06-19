import sys
from sowa.requests.base import SowaRequest
from sowa.static import *
import json

class SowaRecordRequest(SowaRequest):
   def __init__(self, commands, index, previous_record):
      self.index = index
      self.request_type = RECORD_REQUEST
      if previous_record:
         command = commands[0]
         hard_key = previous_record
         soft_key = index
      else:
         hard_key = index
         soft_key = ""
         command = commands[1]
      SowaRequest.__init__(self, command, 21, 15, 5, hard_key, b"\x00", soft_key, b"\x00")
      
   def json_result(self):
      return json.loads(self.result()[6].strip())

   def next(self):
      rec_id = self.result()[0]
      return self.__class__(self.index, rec_id)
      
   def rec_id(self):
      return self.result()[1]+self.json_result()["rec_id"].strip()
      
class SowaFirstRecordRequest(SowaRecordRequest):
   def __init__(self, index = "MA", previous_record = None):
      SowaRecordRequest.__init__(self, [56, 55], index, previous_record)

class SowaLastRecordRequest(SowaRecordRequest):
   def __init__(self, index = "MA", previous_record = None):
      SowaRecordRequest.__init__(self, [58, 57], index, previous_record)

class SowaUpdateTimeRequest(SowaLastRecordRequest):
   def __init__(self, previous_record=None):
      SowaLastRecordRequest.__init__(self, "UT", previous_record)
   def next(self):
      rec_id = self.result()[0]
      return self.__class__(rec_id)
      