from sowa.requests.report import *
class SowaEvent:
   def __init__(self, action, id):
      self.action = action
      self.id     = id
      
   def to_array(self, array = {}):
      return {"id":self.id, "action":self.action, "data":array}
      
class SowaRecordEvent(SowaEvent):
   def __init__(self, action, user, record_id):
      self.user = user
      SowaEvent.__init__(self, action, record_id)

class SowaModificationEvent(SowaRecordEvent):
   def __init__(self, user, record_id):
      SowaRecordEvent.__init__(self, "update-record", user, record_id)
      
   def to_array(self):
      return SowaEvent.to_array(self, {"iso_record" : SowaIsoRequest(self.id).result(), "user" : self.user})

class SowaDeleteEvent(SowaRecordEvent):
   def __init__(self, user, record_id):
      SowaRecordEvent.__init__(self, "delete-record", user, record_id)