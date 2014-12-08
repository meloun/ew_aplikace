'''
Created on 13.11.2013

@author: z002ys1y
'''
cmds = {                                                                
    "GET_HW_SW_VERSION"         : {'cmd':0x04,  'length':0,     'blackbox': True,    'terminal': True},                                      
    "GET_DIAGNOSTIC"            : {'cmd':0x08,  'length':2,     'blackbox': True,    'terminal': False},                                      
    "GET_CALIBRATION_DATA"      : {'cmd':0x0F,  'length':0,     'blackbox': True,    'terminal': False},                                      
    "GET_TERMINAL_INFO"         : {'cmd':0x20,  'length':0,     'blackbox': True,    'terminal': True},                                      
    "GET_CELL_INFO"             : {'cmd':0x21,  'length':1,     'blackbox': True,    'terminal': True},                                      
    "GET_TIMING_SETTINGS"       : {'cmd':0x22,  'length':0,     'blackbox': True,    'terminal': True},                                      
    "GET_RUN_PAR_INDEX"         : {'cmd':0x30,  'length':2,     'blackbox': True,    'terminal': True},                                      
    "GET_TIME_PAR_INDEX"        : {'cmd':0x32,  'length':2,     'blackbox': True,    'terminal': True},
}

#print cmds

#for cmd in sorted(cmds.iteritems(), key=lambda (x, y): y['cmd']):
#    print cmd[1]['cmd'], type(cmd)

print sorted(cmds.iteritems(), key=lambda (x, y): y['cmd'])