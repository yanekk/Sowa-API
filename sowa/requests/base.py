from sowa.connector import SowaConnector
import struct

class SowaRequest:
   def __init__(self, command, *parameters):
      self.__result = None
      self.__request_items = []
      self.__request_items.append(struct.pack('B',command))
      
      for p in parameters:
         if p.__class__ == int:
            self.__request_items.append(struct.pack("i", p))
         elif p.__class__ == str:
            self.__request_items.append(p.encode("cp1250"))
         else:
            self.__request_items.append(p)
            
   def to_request(self):
      req = b""
      for i in self.__request_items:
         req += i
      return req
      
   def set_result(self, result):
      self.__result = result

   def result(self):
      if not self.__result:
         self.do()
      return self.__result
      
   def do(self):
      connector = SowaConnector.instance()
      connector.request(self)
      return self
      
   def type(self):
      return self.request_type