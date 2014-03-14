# -*- coding: utf-8 -*-
'''
Created on 5.2.2014

@author: Meloun
'''
import pandas as pd


df = pd.read_csv("test_input.csv", sep = ";", encoding = 'utf-8')
df.to_csv("test_output.csv", index = False)

#přímý zápis
df.to_excel('output.xlsx', index = False)

#writer a postupné zapisování
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer, index = False)
writer.save()

print df.to_string(index = False)

#vyčte všechny tabulky z www
#url = 'http://www.casomira-ewitis.cz/zavod/blizak-2014/kategorie'
#dfs = pd.read_html(url)
#print dfs
