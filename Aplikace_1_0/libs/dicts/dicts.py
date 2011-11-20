# -*- coding: utf-8 -*-
'''
Created on 17.9.2009
@author: Lubos Melichar

 - operace se seznamy slovniku
'''

#vyparsuje vsechny klice (kazdy pouze jednou)
def fibo():
    print "fibo"
    
def keys(dicts):
    keys = []
    for dict in dicts:
        for key in dict.keys():
            if not(key in keys):
                keys.append(key)
    return sorted(keys)

def keys_values(dicts):
    data = {'keys':keys(dicts), 'values':[]}
    for dict in dicts:
        list = []
        for key in data['keys']:
            if key in dict:
                list.append(dict[key])
            else:
                list.append("-")
        data['values'].append(list)
    return data

def toCsv(dict):    
    CsvString = ""    
    for item in dict.values():
        CsvString = CsvString + str(item) + ";"
    return CsvString

if __name__ == "__main__":
    import dicts
    mujDict={'a':'aa','b':'bb','c':'cc','d':'dd'}
    dicts1 = [{u'klíč1':u"čeština1", u'klíč2':u"maďarština1", u'klíč3':u"francouština1"},
            {u'klíč1':u"čeština2", u'klíč7':u"maďarština2", u'klíč6':u"francouština2"}
            ]
    
    print dicts.toCsv(mujDict)
    print "** "
    keys_values = dicts.keys_values(dicts1)
    print keys_values
    print "**"
    
    for key in keys_values['keys']:
        print key,