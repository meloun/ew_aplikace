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
        #html.html.__init__(self, filename, title, styles, scripts = [""])
        self.lists = lists
        self.keys = keys
        self.table_id = "table_times"                     
    
    #basic function, OVERRIDE
    def get_body(self):
        
        #<H1> title                
        title = htmltags.H1(self.head["title"])                

        #<table> from gui table          
        #print "scripts", self.head[""]                     
        table = self.lists_to_table(self.lists, self.keys, id=self.table_id)        
        
        #<table> into <div>
        div = htmltags.DIV(table, id="table_container")

        #return <body>            
        return htmltags.BODY( title + div )
    
      
if __name__ == "__main__":
    dicts = [{u'klíč1':u"čeština", u'klíč2':u"maďarština", u'klíč3':u"francouština"},
            {u'klíč1':u"čeština", u'klíč3':u"maďarština", u'klíč6':u"francouština"}
            ]
    list = ["a","b"]
    
    html_page = Page_table("index.htm", "TITLES", styles= ["css/results.css",], lists = [["st1", "st2"],["st1", "st2"]], keys = ["sc1","sc2"])
    
    print html_page.get_head()
    html_page.save()
    