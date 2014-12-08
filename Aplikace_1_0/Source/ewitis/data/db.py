'''
Created on 8.12.2013

@author: Meloun
'''

import libs.sqlite.sqlite as sqlite

#=======================================================================
# DATABASE
#=======================================================================
print "I: Database init"
try:           
    db = sqlite.sqlite_db("db/test_db.sqlite")                
    db.connect()
except:
    print "E: Database"
    
