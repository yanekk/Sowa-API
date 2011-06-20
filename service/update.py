import json
class UpdateError(Exception):
   pass
   
class ServiceUpdater:
   def __init__(self, base_url, api_key):
      self.base_url = base_url
      self.api_key  = api_key
      self.events   = []
      self.error    = None
      
   def add_event(self, event):
      self.events.append(event)
      
   def to_json(self):
      result = []
      for event in self.events:
         result.append(event.to_array())
      return json.dumps(result)
      
   def error_message(self):
      return str(self.error)
      
   def update(self):
      try:
         raise UpdateError("Service not implemented... yet :-)")
      except Exception as e:
         self.error = e
         return False
      return True