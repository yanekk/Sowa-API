import re
class LogAnalyzerTimer:
   def __init__(self, day):
      self.day = day
      self.timer_rule = "^{0}.*?$".format(day)
      
   def has_passed(self, line):
      if re.match(self.timer_rule, line, re.IGNORECASE):
         return True
      return False
      
   def stamp(self):
      return self.day