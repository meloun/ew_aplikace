'''
Created on 8.12.2013

@author: Meloun
'''
import ewitis.gui.myModel as myModel


class TestParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Test"  
                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                                            
        

class TestModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
                            

                
    def getDefaultTableRow(self): 
        row = myModel.myModel.getDefaultTableRow(self)                                    
        return row

from manage_gui import uuiA    
tableTest = TestModel(TestParameters(uuiA))