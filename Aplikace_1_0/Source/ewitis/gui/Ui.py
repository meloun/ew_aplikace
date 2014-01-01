# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

@author: Meloun
'''

import sys
from PyQt4 import QtGui
from Ui_App import Ui_MainWindow

class AppWindow(QtGui.QMainWindow):
    def __init__(self):
        pass
    
    def Init(self):                            
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()        
        self.ui.setupUi(self) #insert design from qt designer        
        self.setupUi() #insert my own design
        
    def setupUi(self):
        print "insert my own design"                                                     
            
    def Ui(self):        
        return self.ui
                  
if __name__ != "__main__":
    print "I: Gui init"
    
    #instance       
    appWindow = AppWindow()
        
    def Ui():
        return appWindow.Ui()     
     
if __name__ == "__main__":
    from ewitis.gui.Ui import appWindow
    app = QtGui.QApplication(sys.argv)
    appWindow.Init()    
    appWindow.show()    
    sys.exit(app.exec_())


#DEFAULT CALLING FROM QT DESIGNER
#
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     MainWindow = QtGui.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())



