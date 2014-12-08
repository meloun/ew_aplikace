'''
Created on 8. 12. 2014

@author: Meloun
'''
from xlrd import open_workbook, XL_CELL_NUMBER, XL_CELL_TEXT, XL_CELL_EMPTY
from xlwt import easyxf
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlutils.save import save

def lists2excel(lists, output_filename, template_filename, sheetname = None, sheetindex = 0, offset = [0, 0]):
    
    rb = open_workbook(template_filename, formatting_info = True)
    #print rb.sheet_names()
    
    if (sheetname != None):
        worksheet = rb.sheet_by_name(sheetname)
    else:
        worksheet = rb.sheet_by_index(sheetindex)
        
    for y, row in enumerate(lists):
        for x,item in enumerate(row):
            #print item, type(item)
            if(type(item) is int):               
                worksheet.put_cell(y, x, XL_CELL_NUMBER, item, worksheet.cell_xf_index(y, x))                             
            else:
                worksheet.put_cell(y, x, XL_CELL_TEXT, item, worksheet.cell_xf_index(y, x))
    save(rb, output_filename)
            
            
lists1 = [["a1","a2", "a3"], ["b1", 5, "b3"], ["c1","c2", "c3"]]   
lists2 = [["11","22", "33"], ["12","22", "32"], ["13","23", "33"]]    
lists3 = [[11, 22, u"aa"], [12, 22, u"32s"]]

            
lists2excel( lists3, 'output.xls', 'input.xls', 'NBG Devices', )