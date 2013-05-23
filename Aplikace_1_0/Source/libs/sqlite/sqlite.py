#-*- coding: utf-8 -*-  
'''
Created on 01.06.2010

@author: MELICHARL
'''
#from sqlite3 import dbapi2 as sqlite
import sys
from pysqlite2 import dbapi2 as sqlite
import time

import libs.db_csv.db_csv as Db_csv
import libs.utils.utils as utils


class CSV_FILE_Error(Exception): pass

#SQLITE DATABASE
# - getAll(), getParId(), getParX(), insert_from_lists
class sqlite_db(object):
    def __init__(self, db_name):        
        self.db_name = db_name 
        
    def cursor2list(self, cursor):
        list = []
        for row in cursor:
            list.append(self.dict_factory(cursor, row))
        return list
    
    def cursor2dicts(self, cursor):
        list = []
        for row in cursor:
            dict = self.dict_factory(cursor, row)
            list.append(dict)
        return list
            
                 
        
    
    #convert "db-row" to lists 
    def lists_factory(self, cursor):                
        d = []        
        return d  
    
    #convert "db-row" to dict (to dict can be added record)
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d       
        
    def connect(self):
        self.db = sqlite.connect(self.db_name, 10)        
        self.db.row_factory = sqlite.Row
        
    def commit(self):        
        res = self.db.commit()
        #print "COMMIT:  "                                          
        return res 
            
    def query(self, query):
        #import time                
        query = utils.getUtf8String(query)
        
        #z1 = time.clock()                
        #print "QUERY:  ",query
        #try:
        last_result = self.db.execute(query)
        #except (sqlite.OperationalError)  as (strerror):            
        #    print "E: pysqlite2._sqlite.OperationalError", strerror
        #    print "query: ", query
        #    return None
        #except:
        #    print "E: query fatal error", sys.exc_info()[0]
        #    print "query: ", query
        #    return None
        #print "  - sql take:", (time.clock()-z1)
                        
        return last_result
       
    def getCount(self, tablename):
        query = "SELECT COUNT(*) from " + tablename
        res = self.query(query)
        return res.fetchone()[0]
        
    def getAll(self, tablename):
        query = "SELECT * from " + tablename        
        res = self.query(query)
        return res
    
    def getFirst(self, tablename):                
        query = "SELECT * from " + tablename + " LIMIT 1"         
        res = self.query(query)  
        return res.fetchone()          
        
    def getParId(self, tablename, id):
        query = "select * from " + tablename + " where id = " + str(id) + " LIMIT 1"
        res = self.query(query)
        return res.fetchone()    
    
    def getParX(self, tablename, parameter, value, limit = None):
        query = u"select * from " + tablename + " where \"" + parameter +"\" = '" + unicode(value) + "'"
        query = query + " ORDER BY id DESC " 
        if (limit != None) and (limit != 0):
            query = query + " LIMIT "+str(limit)
        #print  "getParX :", query       
        res = self.query(query)
        return res
    
    # getParXX(conditions, operation) => condition[0][0]=condition[0][1] OPERATION condition[1][0]=condition[1][1]
    def getParXX(self, tablename, conditions, operation, limit = None):
        
        #where_string = (" "+operation+" ").join(condition[0]+" = " + str(condition[1]) for condition in conditions)
        
        conditions_list = []
        
        #list of conditions in format ["id = 5","id = 8",..]
        for condition in conditions:
            conditions_list.append(condition[0]+" = " + (condition[1]))
        
        #separate conditions with 'operator' - AND, OR, ..
        where_string =  (" "+operation+" ").join(conditions_list)
        
        query = "select * from " + tablename + " where " + where_string 
        
        if (limit != None) and (limit != 0):
            query = query + " LIMIT "+str(limit)
        
        res = self.query(query)
        return res
    
    def getMax(self, tablename, parameter):
        query = u"select max("+parameter+") from "+tablename        
        res = self.query(query)
        return res.fetchone()[0]

    ###########
    # INSERT
    ###########
    
    def insert_from_lists(self, tablename, keys, values, commit = True):
                
        
        '''vytvoreni stringu pro dotaz, nazvy sloupcu a hodnot '''  
        values_str = u",".join([u"'"+unicode(x)+u"'" for x in values])        
        #mystring =   u",".join([u" "+unicode(k)+u"='"+unicode(v)+u"'" for k,v in zip(keys, values)])    
        
        keys_str = u",".join(keys)
            
        #print keys_str
        #print values_str
        
        '''sestaveni a provedeni dotazu'''
        query = u"insert into %s(%s) values(%s)" % (tablename, keys_str, values_str)
        query = query.replace('\'None\'', 'Null')
        #print "qq2", query
        
        res = self.query(query)
        
        if(commit == True):
            self.commit()
        return res
    
    '''vlozeni jednoho zaznamu z dict'''
    def insert_from_dict(self, tablename, dict,  commit = True):                
        return self.insert_from_lists(tablename, dict.keys(), dict.values(), commit = commit )        
    
    ###########
    # REPLACE
    ###########
    
    '''nahrazeni jednoho zaznamu z lists'''
    def replace_from_lists(self, tablename, keys, values):
        
        '''vytvoreni stringu pro dotaz, nazvy sloupcu a hodnot '''        
        values_str = u",".join([u"'"+unicode(x)+u"'" for x in values])
        keys_str = u",".join(keys)
            
        #print keys_str
        #print values_str
        
        '''sestaveni a provedeni dotazu'''
        query = u"replace into %s(%s) values(%s)" % (tablename, keys_str, values_str)
        res = self.db.query(query)
        self.db.commit()
        return res
    
    
    ###########
    # UPDATE
    ###########
    # - update users SET  category="Kat D", nr="4" WHERE id = "4"
    # - record has to exist

    def update_from_lists(self, tablename, keys, values):
        
        #print keys
        #print values
        
        res = '' 
                       
        '''vytvoreni stringu pro dotaz, 
        column1=value, column2=value2,... '''                      
        mystring = u",".join([u" "+unicode(k)+unicode(u)+"='"+unicode(v)+unicode(u)+"'" for k,v in zip(keys, values)])                            
        
        '''sestaveni a provedeni dotazu'''
        query = u"update %s SET %s WHERE id = \"%s\"" % (tablename, mystring, values[0])        
        res = self.query(query)
        self.db.commit()
            
        return res
    
    def update_from_dict(self, tablename, dict, commit = True):                        
    
        keys = dict.keys()
        values = dict.values()
                
        res = ''                 
                           
        '''vytvoreni stringu pro dotaz, 
        column1=value, column2=value2,... '''                                        
        mystring = u",".join([u" "+unicode(k)+u"='"+unicode(v)+u"'" for k,v in zip(keys, values)])
                        
        
        #print "mystring", mystring
                
        '''sestaveni a provedeni dotazu'''
        query = u"update %s SET %s WHERE id = \"%s\"" % (tablename, mystring, dict['id']) 
        query = query.replace('\'None\'', 'Null')                                       
              
        res = self.query(query)
        if commit == True:      
            self.commit()            
        return res
        

    ###########
    # DELETE
    ###########                
    def delete(self, tablename, id):
        query = "delete from " + tablename + " where id = " + str(id)        
        res = self.query(query)
        self.commit()
        
    def deleteAll(self, tablename):
        query = "delete from " + tablename        
        res = self.query(query)
        self.commit()
        
    def deleteParX(self, tablename, parameter, value):
        query = "delete from " + tablename + " where " + parameter +" = " + str(value)          
        res = self.query(query)
        self.commit()        
        
        
    #=============
    # IMPORT
    #=============
    # exception: CSV_FILE_Error (check the first line => header)
    #
    def importCsv(self, tablename, filename, keys):
                                
        #create DB        
        aux_csv = Db_csv.Db_csv(filename)
        rows =  aux_csv.load()
        
        #counters
        state = {'ko':0, 'ok':0}                        
        
        #wrong file format?
        if (rows==[]):
            raise CSV_FILE_Error
        
        #header, check first X keys
        header = rows.pop(0)
        print "header> ", header
        print "keys> ",keys
        for i in range(3): 
            if not(header[i] in keys):
                raise CSV_FILE_Error
            
        for row in rows:                                                              
                                                      
            #ADD USER
            try:
                print "import row", dict(zip(keys, row))                              
                #dict(zip()) - synchronize lists to dictionary 
                self.insert_from_dict(tablename, dict(zip(keys, row)), commit = False)                      
                #self.insert_from_lists(tablename, keys, row, commit = False) 
                state['ok'] += 1            
            except:
                state['ko'] += 1 #increment errors for error message

        self.commit()                        
        
        return state             
        
if __name__ == "__main__":
    import json
  
    print "start"
    
    '''define db and tables'''
    db = sqlite_db("test_db.sqlite")       
    
    '''connect to db'''  
    db.connect()    
       
   