from distutils.core import setup 
import py2exe 
setup(    
    options={
       "py2exe" : {"includes" : ["sip",]}
    },
    data_files = [
      ('imageformats', [
        r'C:\programs\Python271\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll'
        ])],
    console=[{          
       "script" : "manage_gui.py",
       "icon_resources": [(1, "ewitis_favicon.ico")]
    }]
) 