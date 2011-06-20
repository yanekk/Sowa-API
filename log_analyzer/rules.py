# -*- coding: utf-8 -*-
import re
from service.events import *

class LogAnalyzerRule:
   SOWA_HEADER = "^\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2} \* "
   def __init__(self, service_updater):
      self.service_updater = service_updater
      
   def rule(self):
      raise NotImplementedError()
      
   def check(self, line):
      if re.match(self.rule(), line, re.IGNORECASE):
         self.act(line)
         
   def act(self, line):
      raise NotImplementedError()
      

class PrintRule(LogAnalyzerRule):
   def rule(self):
      return "^.*$"
      
   def act(self, line):
      print(line)

class SowaDeleteRule(LogAnalyzerRule):
   def rule(self):
      rule = LogAnalyzerRule.SOWA_HEADER+"\d+?: Użytkownik: (.*?) usunął rekord: (.*?)$"
      return rule
      
   def act(self, line):
      self.service_updater.add_event(SowaDeleteEvent(*re.match(self.rule(), line).groups()))

class SowaModificationRule(LogAnalyzerRule):
   def rule(self):
      rule = LogAnalyzerRule.SOWA_HEADER+"\d+?: Użytkownik: (.*?) zmodyfikował rekord: (.*?)$"
      return rule
      
   def act(self, line):
      self.service_updater.add_event(SowaModificationEvent(*re.match(self.rule(), line).groups()))