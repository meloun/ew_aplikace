# -*- coding: utf-8 -*-

'''
Created on 17.4.2011
@author: Lubos Melichar
'''

import libs.html.html as html
import libs.html.htmltags as htmltags

#user title
TITLE = "Kralovický MTB maraton 2011"

#
class Page_table(html.html):
    
    def __init__(self, filename, title=TITLE, styles=None, scripts=None, lists=None, keys = None):
        html.html.__init__(self, filename, title, styles, scripts)        
        self.lists = lists
        self.keys = keys                     
    
    #basic function, OVERRIDE
    def get_body(self):
        
        #<H1> title                
        title = htmltags.H1(self.head["title"])                

        #<table> from gui table                               
        table = self.lists_to_table(self.lists, self.keys)
        
        #<table> into <div>
        div = htmltags.DIV(table, id="table_container")

        #return <body>            
        return htmltags.BODY( title + div )
    
      
if __name__ == "__main__":
    dicts = [{u'klíč1':u"čeština", u'klíč2':u"maďarština", u'klíč3':u"francouština"},
            {u'klíč1':u"čeština", u'klíč3':u"maďarština", u'klíč6':u"francouština"}
            ]
    list = ["a","b"]
    
    html_page = ewitis_html("index.htm", "TITLES", ["st1", "st2"], ["sc1","sc2"])
    
    print html_page.get_head()
    html_page.save(["jedna","dva"])
    
    #print dicts_to_table(dictss)
    #print html_page.dicts_to_table(dicts, ["klíč1", 'klíč2'])
    #print html_page.list_to_table(list)t html_page.list_to_table(list)