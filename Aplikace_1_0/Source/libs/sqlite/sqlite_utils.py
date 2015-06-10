#-*- coding: utf-8 -*-  
'''
Created on 01.06.2010commit


@author: MELICHARL
'''
import sys
from pysqlite2 import dbapi2 as sqlite
#from sqlite3 import dbapi2 as sqlite #older, less patches, slowly
import libs.utils.utils as utils
       
        
def connect(filename):
    db = sqlite.connect(filename, 5)        
    db.row_factory = sqlite.Row
    return db
        
def commit(db):                
    res = db.commit()                                                  
    return res 
            
def query(db, query_string):
                    
    query_string = utils.getUtf8String(query_string)
    
    #z1 = time.clock()                
    #print "QUERY:  ",query_string
    #try:
    last_result = db.execute(query_string)
#     except (sqlite.OperationalError)  as (strerror):            
#         print "E: pysqlite2._sqlite.OperationalError", strerror
#         print "query: ", query_string
#         return None
    #print "  - sql take:", (time.clock()-z1)                    
    return last_result
       
def getCount(db, tablename):
    query_string = "SELECT COUNT(*) from " + tablename
    res = query(db, query_string)        
    return res.fetchone()[0]
        
def getAll(db, tablename):
    query_string = "SELECT * from " + tablename        
    res = query(db, query_string)
    return res
    
def getFirst(db, tablename):                
    query_string = "SELECT * from " + tablename + " LIMIT 1"         
    res = query(db, query_string)  
    return res.fetchone()          
        
def getParId(db, tablename, id):
    query_string = "select * from " + tablename + " where id = " + str(id) + " LIMIT 1"
    res = query(db, query_string)
    if res != None:
        res = res.fetchone() 
    return res    

def getParX(db, tablename, parameter, value, limit = None):
    query_string = u"select * from " + tablename + " where \"" + parameter +"\" = '" + unicode(value) + "'"
    query_string = query_string + " ORDER BY id DESC " 
    if (limit != None) and (limit != 0):
        query_string = query_string + " LIMIT "+str(limit)
    #print  "getParX :", query       
    res = query(db, query_string)
    return res
    
# getParXX(conditions, operation) => condition[0][0]=condition[0][1] OPERATION condition[1][0]=condition[1][1]
def getParXX(db, tablename, conditions, operation, limit = None):
    
    #where_string = (" "+operation+" ").join(condition[0]+" = " + str(condition[1]) for condition in conditions)
    
    conditions_list = []
    
    #list of conditions in format ["id = 5","id = 8",..]
    for condition in conditions:
        if (type(condition[1]) is str):
            condition[1] = "\'"+ condition[1] + "\'"
        conditions_list.append(condition[0]+" = " + (condition[1]))
    
    #separate conditions with 'operator' - AND, OR, ..
    where_string =  (" "+operation+" ").join(conditions_list)
    
    query_string = "select * from " + tablename + " where " + where_string 
    
    if (limit != None) and (limit != 0):
        query_string = query_string + " LIMIT "+str(limit)
    
    res = query(db, query_string)
    return res
    
def getMax(db, tablename, parameter):
    query_string = u"select max("+parameter+") from "+tablename        
    res = query(db, query_string)
    return res.fetchone()[0]

def getCollumnNames(db, tablename):
    query_string = u"select * from "+tablename        
    res = query(db, query_string)
    return list(map(lambda x: x[0], res.description))

# ###########
# # INSERT
# ###########
#     
# def insert_from_lists(self, tablename, keys, values, commit_flag = True):
#             
#     ret = True
#     
#     '''vytvoreni stringu pro dotaz, nazvy sloupcu a hodnot '''  
#     values_str = u",".join([u"'"+unicode(x)+u"'" for x in values])   
#     keys_str = u",".join([u"'"+unicode(x)+u"'" for x in keys])
#     
#     '''sestaveni a provedeni dotazu'''
#     query_string = u"insert into %s(%s) values(%s)" % (tablename, keys_str, values_str)
#     query_string = query_string.replace('\'None\'', 'Null')    
#             
#     try:
#         query(query_string)
#     except sqlite.IntegrityError:
#         ret = False  #this entry probably already exist
#     except:
#         print "E: DB: insert from lists, some error"
#         ret = False
#     
#     if(commit_flag == True):
#         commit()
#     return ret
#     
# '''vlozeni jednoho zaznamu z dict'''
# def insert_from_dict(self, tablename, dict,  commit_flag = True):                
#     return self.insert_from_lists(tablename, dict.keys(), dict.values(), commit_flag = commit )        
    
# ###########
# # REPLACE
# ###########
# 
# '''nahrazeni jednoho zaznamu z lists'''
# def replace_from_lists(self, tablename, keys, values):
#     
#     '''vytvoreni stringu pro dotaz, nazvy sloupcu a hodnot '''        
#     values_str = u",".join([u"'"+unicode(x)+u"'" for x in values])
#     keys_str = u",".join(keys)
#         
#     #print keys_str
#     #print values_str
#     
#     '''sestaveni a provedeni dotazu'''
#     query = u"replace into %s(%s) values(%s)" % (tablename, keys_str, values_str)
#     res = self.db.query(query)
#     self.db.commit()
#     return res
    
    
###########
# UPDATE
###########
# - update users SET  category="Kat D", nr="4" WHERE id = "4"
# - record has to exist

def update_from_dict(db, tablename, dict, commit_flag = True):                        

    keys = dict.keys()
    values = dict.values()               
                       
    '''vytvoreni stringu pro dotaz, 
    column1=value, column2=value2,... '''                                        
    mystring = u",".join([u" "+unicode(k)+u"='"+unicode(v)+u"'" for k,v in zip(keys, values)])
            
    '''sestaveni a provedeni dotazu'''
    query_string = u"update %s SET %s WHERE id = \"%s\"" % (tablename, mystring, dict['id']) 
    query_string = query_string.replace('\'None\'', 'Null')
                                           
    
    res = query(db, query_string)        
    if commit_flag == True:  #musi tu byt! napr. zmena kategorie, zapis do db                           
        commit(db)                                               
                
    return res    

# def update_from_lists(self, tablename, keys, values):
#     
#     #print keys
#     #print values
#     
#     res = '' 
#                    
#     '''vytvoreni stringu pro dotaz, 
#     column1=value, column2=value2,... '''                      
#     mystring = u",".join([u" "+unicode(k)+unicode(u)+"='"+unicode(v)+unicode(u)+"'" for k,v in zip(keys, values)])                            
#     
#     '''sestaveni a provedeni dotazu'''
#     query = u"update %s SET %s WHERE id = \"%s\"" % (tablename, mystring, values[0])        
#     res = self.query(query)
#     self.db.commit()
#         
#     return res
    

        

###########
# DELETE
###########                
def delete(db, tablename, id):
    query_string = "delete from " + tablename + " where id = " + str(id)        
    res = query(db, query_string)
    commit(db)
    
def deleteAll(db, tablename):
    query_string = "delete from " + tablename        
    res = query(db, query_string)
    commit(db)
    

        
if __name__ == "__main__":
  
    
    '''define db and tables'''
    db = connect("db/test_db.sqlite")       
    
    '''connect to db'''  
        
    print getFirst(db, "times")