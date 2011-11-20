'''
Created on 01.06.2010

@author: MELICHARL
'''
#-*- coding: utf-8 -*- 


def get_query_times_par_id(id):
    return ""+ \
        "SELECT * FROM times "+\
        "INNER JOIN runs ON runs.id = times.run_id "+ \
        "WHERE runs.id="+str(id)