import os, time
class LogAnalyzer:
   def __init__(self, log_path, timer=None, encoding="CP1250"):
      self.log_path = log_path
      self.log_file = open(log_path, "r", encoding=encoding)
      self.rules = []
      self.timer = timer
      
   def analyze(self):
      line = self.log_file.readline()
      while(line):
         if self.timer:
            if not self.timer.has_passed(line):
               line = self.log_file.readline()
               continue
         for rule in self.rules:
            rule.check(line.strip())
         line = self.log_file.readline()
         
   def add_rule(self, rule):
      self.rules.append(rule)
      
   def rename(self):
      self.close()
      file_name = os.path.basename(self.log_path)
      dir_name  = os.path.dirname(self.log_path)
      if(self.timer):
         new_name = "{0}.{1}".format(file_name, self.timer.stamp())
      else:
         new_name = "{0}.{1}".format(file_name, time.strftime("%d%m%Y"))
      os.rename("{0}/{1}".format(dir_name,file_name), "{0}/{1}".format(dir_name, new_name))
      
   def close(self):
      self.log_file.close()