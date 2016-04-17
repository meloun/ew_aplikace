# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

@author: Meloun
'''

import sys
from PyQt4 import QtGui, QtCore
from Ui_App import Ui_MainWindow

from ewitis.data.dstore import dstore
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class AppWindow(QtGui.QMainWindow):
    def __init__(self):
        pass
    
    def Init(self):                            
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        
        #insert design from qt designer        
        self.ui.setupUi(self)
                 
        #insert my own design
        self.setupUi()      
        
    def setupUi(self): 
        self.ui.TimesAutoNumber1.installEventFilter(self)
        self.ui.TimesAutoNumber2.installEventFilter(self)
        self.ui.TimesAutoNumber3.installEventFilter(self)
        self.ui.TimesAutoNumber4.installEventFilter(self)
        self.installEventFilter(self)
               
        self.ui.statusbar_msg = QtGui.QLabel("configuring..")        
        self.ui.statusbar_time = QtGui.QLabel("00:00:00,00")        
        self.ui.statusbar.addPermanentWidget(self.ui.statusbar_time)    
        self.ui.statusbar.addPermanentWidget(self.ui.statusbar_msg)    
        self.ui.webViewApp.setUrl(QtCore.QUrl(_fromUtf8("doc\Návod\Aplikace Návod.html")))                                    
        self.setWindowTitle(QtGui.QApplication.translate("MainWindow", u"Časomíra Ewitis, Aplikace "+dstore.Get("versions")["app"], None, QtGui.QApplication.UnicodeUTF8))
        
    def eventFilter____1(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            if source is self.ui.TimesAutoNumber1:
                print "1: ",
            elif source is self.ui.TimesAutoNumber2:
                print "2: ",
            elif source is self.ui.TimesAutoNumber3:
                print "3: ",
            elif source is self.ui.TimesAutoNumber4:
                print "4: ",
            else:
                print "x: ", source
                 
            print('key pressed: %s' % event.text())
            if (event.key() == QtCore.Qt.Key_Return) or (event.key() == QtCore.Qt.Key_Enter): 
                print 'Enter pressed', source
            elif(event.key() == QtCore.Qt.Key_Insert):
                print 'Insert pressed', source
             
 
                 
            return True        
        return QtGui.QMainWindow.eventFilter(self, source, event)
    
    #def keyPressEvent(self, qKeyEvent):
    #    print "keyPressEvent"
                         
    def Ui(self):        
        return self.ui
                  
if __name__ != "__main__":
    print "I: Gui init"
    
    #instance       
    appWindow = AppWindow()
        
    def Ui():
        return appWindow.Ui()     
     
if __name__ == "__main__":
    #print "IMPORTUJI", __name__
    #from ewitis.gui.Ui import appWindow
    app = QtGui.QApplication(sys.argv)
        
    appWindow = AppWindow()
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



