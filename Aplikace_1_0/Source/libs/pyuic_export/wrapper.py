# -*- coding: utf-8 -*-
'''
Created on 8.11.2009

@author: Lubos Melichar
'''
from PyQt4 import QtCore, QtGui
import button

class MyClass(object):
    def __init__(selfparams):
        '''
        Constructor

        '''
def button_slot():
    print "button clicked"
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = button.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.pushButton.setText("ahojky")
    
    app.connect(ui.pushButton,QtCore.SIGNAL("clicked ()"),button_slot)
    
    MainWindow.show()
    sys.exit(app.exec_())        