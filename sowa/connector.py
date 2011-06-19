import socket, struct
from sowa.static import *
class SowaConnector: 
   __instance = None
   
   def __init__(self, host, port):
      self.__host = host
      self.__port = port
      self.__connect()
      
   @classmethod
   def connect(cls, host, port):
      connection = SowaConnector(host, port)
      SowaConnector.__instance = connection
      
   @classmethod
   def instance(cls):
      if not SowaConnector.__instance:
         raise Exception("SowaConnector singleton instance is not instatiated")
         
      return SowaConnector.__instance
      
   def __connect(self):
      self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.__socket.settimeout(5.0)
      self.__socket.connect((self.__host, self.__port))
      self.__socket.setblocking(1)
      self.__socket.send(b"\x1E")
      self.read_all();

   def read_all(self):
      result = b"";
      char = self.__socket.recv(1)

      while (char != b"\x00"):
         result += char
         char = self.__socket.recv(1)

      return result.decode("cp1250");
      
   def get_record_response(self, request):
      size = struct.unpack("i", self.__socket.recv(4))[0]
      result = []
      for i in range(size):
         result.append(self.read_all())
      return result
      
   def get_report_response(self, request):
      packets    = struct.unpack("i", self.__socket.recv(4))[0]
      packetsize = struct.unpack("i", self.__socket.recv(4))[0]
      result = self.__socket.recv(packetsize)
      return result.decode("cp1250")
      
   def request(self, request):
      r = request.to_request()
      self.__socket.send(r)
      result = getattr(self, "get_{0}_response".format(request.type()))(r)

      request.set_result(result)
      return request
      
   def disconnect():
      self.__socket.write("\x00")
