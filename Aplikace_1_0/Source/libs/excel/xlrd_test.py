'''
Created on 08.10.2014

@author: z002ys1y
'''

import os

from xlrd import open_workbook, XL_CELL_NUMBER
from xlwt import easyxf
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlutils.save import save


        
print "start"
rb = open_workbook('mo_equipment.xls', formatting_info = True)
print rb.sheet_names()
worksheet = rb.sheet_by_name('NBG Devices')
worksheet.put_cell(0, 0, XL_CELL_NUMBER, 2.6, worksheet.cell_xf_index(0, 0))
save(rb,'mo_equipment_rd.xls')

wb = copy(rb)
w_sheet = wb.get_sheet(0)
#w_sheet.put_cell(0, 0, XL_CELL_NUMBER, 2.6, w_sheet.cell_xf_index(0, 0))

print type(w_sheet.row(0))
print type(worksheet.cell(0,0))
#._Row__cells.get(0))
#.xf_idx
#old = w_sheet.get_cell(0,0).xf_idx
w_sheet.write(0,0, 'ou yeah2')
#w_sheet._Worksheet__rows.get(0)._Row__cells.get(0).xf_idx = old


wb.save('mo_equipment_wt.xls')



'''
worksheet = rb.sheet_by_name('NBG Devices')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0
curr_cell = 0

while curr_row < worksheet.nrows:
    row = worksheet.row(curr_row)
    print 'Row:', curr_row
    while curr_cell < num_cells:
        curr_cell += 1
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        print '    ', worksheet.cell_type(curr_row, curr_cell), ':', worksheet.cell_value(curr_row, curr_cell)
    curr_cell = 0
    curr_row += 1
    
save(rb,'mo_equipment_rd.xls')
        
wb = copy(rb)
w_sheet = wb.get_sheet(0)

row = worksheet._Worksheet__rows.get(rowIndex)
print type(row)
cell = row._Row__cells.get(colIndex)
print type(cell)

#print type(worksheet.cell(0,0))
#w_sheet.write(0,0,'ou yeah2', rb.xf_list[worksheet.cell_xf_index(0,0)])

wb.save('mo_equipment_wt.xls')
'''





