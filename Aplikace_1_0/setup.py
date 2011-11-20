from distutils.core import setup 
import py2exe 
setup(console=[{"script" : "manage_gui.py"}], options={"py2exe" : 
{"includes" : ["sip",]}}) 