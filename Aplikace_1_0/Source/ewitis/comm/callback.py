# -*- coding: utf-8 -*-

import serial
import time
import struct
import binascii
import libs.file.file as file
import libs.db.db_json as db
import libs.comm.serialprotocol as serialprotocol
import libs.html.htmltags as htmltags
import libs.html.html as html
import libs.utils.utils as utils
import ewitis.comm.DEF_COMMANDS as DEF_COMMANDS

#===============================================================================
# COMMANDS
#===============================================================================
#CMD_SET_BACKLIGHT       =   0x10
#CMD_SET_TIME            =   0x12
#CMD_GET_RUN_PAR_INDEX   =   0x30
#CMD_GET_TIME_PAR_INDEX  =   0x32

#===============================================================================
# CALLBACK
#===============================================================================
def callback(command, data):
    
    # GET TIME PAR INDEX
    if(command == (DEF_COMMANDS.DEF_COMMANDS["GET"]["time_par_index"] | 0x80)):
        ''' GET_TIME_PAR_IDNEX => TIME struct (16b) + 2b error
            | error (2b) | state(1b) | id (4b) | run_id (2b) | user_id (4b) | cell (1b) | time(4b) |
        '''                                          
        aux_time = {}        
        aux_time['error'], aux_time['state'], aux_time['id'],  aux_time['run_id'], \
        aux_time['user_id'], aux_time['cell'],aux_time['time_raw'], = struct.unpack("<HBIHIBI", data)
        
        #add data
        aux_time['time'] = utils.time_to_string(aux_time['time_raw'])        
                                                        
                       
        return aux_time
    
    # GET RUN PAR INDEX
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET"]["run_par_index"] | 0x80)):        
        ''' GET_RUN_PAR_IDNEX RESPONSE => error(2b) + RUN struct (16b)
            | error (2b) | state(1b) | id (4b) | starttime_id (4b) | datetime (6b) | name_id (1b) 
        '''                                          
        aux_run = {}
        aux_datetime = {}        
        aux_run['error'], aux_run['state'], aux_run['id'],  aux_run['starttime_id'], \
        aux_datetime['sec'], aux_datetime['min'],aux_datetime['hour'],aux_datetime['day'],aux_datetime['month'],aux_datetime['year'],\
        aux_run['name_id'] = struct.unpack("<HBIIBBBBBBB", data)
        
        #add data      
        #aux_run['datetime'] =  '{0}.{1} {2}  {3}:{4}:{5}'.format(aux_datetime['day'], aux_datetime['month'], int(aux_datetime['year'])+2000,aux_datetime['hour'],aux_datetime['min'],aux_datetime['sec'])
        aux_run['datetime'] = '%d.%d. %d %02d:%02d:%02d' % (aux_datetime['day'], aux_datetime['month'], int(aux_datetime['year'])+2000,aux_datetime['hour'],aux_datetime['min'],aux_datetime['sec'])                                                                                  
        return aux_run
    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET"]["terminal_info"] | 0x80)):
        ''' GET_TERMINAL_INFO RESPONSE
            | number_of_cells (1B) | battery (1B)| backlight (1B) | speaker (1B) | language (1B)
        ''' 
        aux_terminal_info = {}
        
        aux_terminal_info['number_of_cells'], aux_terminal_info['battery'], aux_terminal_info['backlight'],  aux_speaker, \
        aux_terminal_info['language'], = struct.unpack("<BBBBB", data)
        
        aux_terminal_info['speaker'] = {}
        aux_terminal_info['speaker']['keys'] = bool(aux_speaker & 0x01)
        aux_terminal_info['speaker']['system'] = bool(aux_speaker & 0x02)
        aux_terminal_info['speaker']['timing'] = bool(aux_speaker & 0x04)
        aux_terminal_info['backlight'] = bool(aux_terminal_info['backlight'])                
                                
        return aux_terminal_info
    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET"]["timing_settings"] | 0x80)):
        ''' GET_TIMING_SETTINGS RESPONSE
            | timing_logic_mode (1B) | measurement_state (1B)| name_id (1B) | basic_tag_timefilter (1B) |
              lap_timefilter (2B) | lap_numberfilter(1B) | 
        ''' 
        aux_timing_settings = {}
        
        aux_timing_settings['logic_mode'], aux_timing_settings['measurement_state'], aux_timing_settings['name_id'],  aux_timing_settings['filter_tagtime'],\
        aux_timing_settings['filter_minlaptime'], aux_timing_settings['filter_maxlapnumber'], = struct.unpack("<BBBBhB", data)                
                                                        
        return aux_timing_settings
        
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET"]["backlight"] | 0x80)):        
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET"]["timing_settings"] | 0x80)):        
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET"]["generate_starttime"] | 0x80)):        
        return data    

    print "d:", data
    return "E: callback error, cmd: " + str(command) 