# -*- coding: utf-8 -*-
from distutils.core import setup 
import py2exe 
import sys  
reload(sys)
if hasattr(sys,"setdefaultencoding"):
  sys.setdefaultencoding("latin-1")
  
  
setup(console=[{"script" : "test.py"}], options={"py2exe" :  
{"includes" : ["sip",
               'encodings',
               'encodings.ascii',
               'encodings.utf_8',
               'encodings.cp866']}}) 