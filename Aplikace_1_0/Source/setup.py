from distutils.core import setup 
import py2exe
import os
import matplotlib

setup(    
    options={
       "py2exe" : {
			 		"includes" : ["sip", "PyQt4.QtNetwork"]			 		
          }			 		
    },
    data_files = matplotlib.get_py2exe_datafiles(),
    console=[{          
       "script" : "manage.py"       
    }]
) 