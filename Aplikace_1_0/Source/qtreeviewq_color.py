'''
Created on 20. 6. 2018

@author: Meloun
'''
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

app = QApplication(sys.argv) 
def main():    
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
 
class MyWindow(QTableView):
    def __init__(self, *args):
        QTableView.__init__(self, *args)
        
        model = QtGui.QStandardItemModel(0, 2)
        self.setModel(model)
    
        for i in range(0,6):
            newRow = model.rowCount();
            model.insertRow(newRow);
    
        # paint first two rows
        for i in range(0, 2):
            model.setData(model.index(i, 0), QBrush(Qt.red), QtCore.Qt.BackgroundRole)
            model.setData(model.index(i, 1), QBrush(Qt.red), QtCore.Qt.BackgroundRole)
 
 
if __name__ == "__main__":
   main()