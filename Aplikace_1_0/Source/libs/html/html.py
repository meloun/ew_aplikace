# -*- coding: utf-8 -*-

'''
Created on 17.9.2009
@author: Lubos Melichar
'''
import libs.file.file as file  
import libs.html.htmltags as htmltags
import libs.dicts.dicts as dicts
import libs.utils.utils as utils

class html(object):
    def __init__(self, filename, title=None, styles=None, scripts=None):
        
        #file        
        self.file = file.File(filename)
    
        #HTML hlavicka    
        self.head = {'title':title, 'styles':styles, 'scripts':scripts}          
        
    def get_head(self):            
        
        aux_head = htmltags.HEAD( htmltags.META(http_equiv="Content-Type", content="application/xhtml+xml; charset=utf-8") )
        aux_head <= htmltags.TITLE(self.head['title'])
        
        if(self.head['styles']):
            for style in self.head['styles']:
                aux_head <= htmltags.LINK(rel="Stylesheet",href=style)
                
        if(self.head['scripts']):
            for script in self.head['scripts']:
                aux_head <= htmltags.LINK(rel="Stylesheet",href=script)
        return aux_head
    
    #basic function, OVERRIDE
    def get_body(self):
        return htmltags.BODY("body")
    
    def save(self):                
        html_string = str(htmltags.HTML(self.get_head()+self.get_body()))        
        self.file.write(html_string)         

    def list_to_table(self, list):
        
        #cellpadding="6" cellspacing="0"
        tabulka = htmltags.TABLE(cellpadding="6", cellspacing="0")        
        
        for i in range(0,len(list)):
            radek = htmltags.TR(htmltags.TD(i))        
            radek <= htmltags.TD( str(list[i]))
            tabulka <= radek        
        return tabulka
    
    # keys  => one row, <TH> 
    # lists =>   N row, <TD>
    def lists_to_table2(self, lists, keys = None, css_class = ""):
        
        tabulka = htmltags.TABLE(cellpadding="6", cellspacing="0",Class=css_class)
        
        #ZAHLAVI, klice - nadpisy sloupcu      
        zahlavi = htmltags.TR()  # inicializace proměnné        
                
        for key in keys:        
            zahlavi <= htmltags.TH(key)
            
        tabulka <= zahlavi
            
        #radky
        for list in lists:
            radekTabulky = htmltags.TR()  # inicializace proměnné                
            for item in list:  # pres vsechny existujici slovniky v datech                                        
                radekTabulky <= htmltags.TD(item)                
            tabulka <= radekTabulky        
                          
        return tabulka
    
    # keys  => one row, <TH> 
    # lists =>   N row, <TD>
    def lists_to_table(self, lists, keys = None, css_class = ""):
        
        tabulka = htmltags.TABLE(cellpadding="6", cellspacing="0",Class=css_class)
                        
        
        #ZAHLAVI, klice - nadpisy sloupcu      
        zahlavi = htmltags.TR()  # inicializace proměnné

        
        
        for key in keys:        
            zahlavi <= htmltags.TH(key)
            
        tabulka <= zahlavi
            
        #radky        
        for list in lists:            
            radekTabulky = htmltags.TR()  # inicializace proměnné  
            for item in list:
                radekTabulky <= htmltags.TD(item)                          
            tabulka <= radekTabulky                    
                          
        return tabulka
    
    def dicts_to_table(self, dicts, keys_to_show, css_class = ""):
        
        tabulka = htmltags.TABLE(cellpadding="6", cellspacing="0",Class=css_class)
        
        #ZAHLAVI, klice - nadpisy sloupcu      
        '''zahlavi = htmltags.TR()  # inicializace proměnné
        for key in keys_to_show:        
            zahlavi <= htmltags.TH(key)
            
        tabulka <= zahlavi
        '''
    
        #radky
        for dict in dicts:
            radekTabulky = htmltags.TR()  # inicializace proměnné                
            for key in keys_to_show:  # pres vsechny existujici slovniky v datech                        
                if key in dict:
                    radekTabulky <= htmltags.TD(dict[key])
                else:
                    radekTabulky <= htmltags.TD('-')  #tento klic ve slovniku neni => '-'
            tabulka <= radekTabulky        
                          
        return tabulka


if __name__ == "__main__":
    dicts = [{u'klíč1':u"čeština", u'klíč2':u"maďarština", u'klíč3':u"francouština"},
            {u'klíč1':u"čeština", u'klíč3':u"maďarština", u'klíč6':u"francouština"}
            ]
    list = ["a","b","c"]
    lists = [["0,0","0,1","0,2"],["1,0","1,1","1,2"]]
    
    html_page = html("index.htm", "TITLES", ["st1", "st2"], ["sc1","sc2"])
    
    print "LISTS: ",html_page.lists_to_table(lists, list)
    print html_page.get_head()
    html_page.save()
    
    #print dicts_to_table(dictss)
    #print html_page.dicts_to_table(dicts, ["klíč1", 'klíč2'])
    #print html_page.list_to_table(list)
    
        