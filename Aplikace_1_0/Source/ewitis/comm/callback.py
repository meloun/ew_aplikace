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
# CALLBACK
#===============================================================================
def unpack_data(command, data, senddata):
    
    #print "callback", hex(command),hex(command-0x80) if command>0x80 else hex(command), data.encode('hex'), len(data)
    
    # HW & FW VERSIONS
    if(command == (DEF_COMMANDS.DEF_COMMANDS["GET_HW_SW_VERSION"]["cmd"] | 0x80)):    
        aux_versions = {}
        aux_versions['hw1'], aux_versions['hw2'],aux_versions['hw3'], aux_versions['fw1'],  aux_versions['fw2']\
        = struct.unpack("<cc2s2s2s", data)        
        
        #some sugar
        if aux_versions['hw1']== 'T':
            aux_versions['hw1'] = 'Terminal'
        elif aux_versions['hw1']== 'B':
            aux_versions['hw1'] = 'Blackbox'
        #    
        aux_versions = {"hw": aux_versions['hw1']+' '+aux_versions['hw2']+'.'+aux_versions['hw3'],
                        "fw":aux_versions['fw1']+'.'+aux_versions['fw2']
                        } 
        return aux_versions
        
        
    # GET TIME PAR INDEX
    if(command == (DEF_COMMANDS.DEF_COMMANDS["GET_TIME_PAR_INDEX"]["cmd"] | 0x80)):
        ''' GET_TIME_PAR_IDNEX => TIME struct (16b) + 2b error
            | error (2b) | state(1b) | id (4b) | run_id (2b) | user_id (4b) | cell (1b) | time(4b) |
        '''                                          
        aux_time = {}        
        aux_time['error'], aux_time['state'], aux_time['id'],  aux_time['run_id'], \
        aux_time['user_id'], aux_time['cell'],aux_time['time_raw'], = struct.unpack("<HBIHIBI", data)
        
        #pricteni casu ke vsem casum, chyba blizak
        #if(aux_time['cell'] != 1):
        #    aux_time['time_raw'] = aux_time['time_raw'] + 255800

        #add data
        aux_time['time'] = None        
                                                                               
        return aux_time
    
    # GET RUN PAR INDEX
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_RUN_PAR_INDEX"]["cmd"] | 0x80)):        
        ''' GET_RUN_PAR_IDNEX RESPONSE => error(2b) + RUN struct (16b)
            | error (2b) | state(1b) | id (4b) | starttime_id (4b) | datetime (6b) | name_id (1b) 
        '''                                          
        aux_run = {}
        aux_datetime = {}        
        aux_run['error'], aux_run['state'], aux_run['id'],  aux_run['starttime_id'], \
        aux_datetime['sec'], aux_datetime['min'], aux_datetime['hour'], aux_datetime['day'], aux_datetime['month'], aux_datetime['year'],\
        aux_run['name_id'] = struct.unpack("<HBIIBBBBBBB", data)
        
        #add data      
        #aux_run['datetime'] =  '{0}.{1} {2}  {3}:{4}:{5}'.format(aux_datetime['day'], aux_datetime['month'], int(aux_datetime['year'])+2000,aux_datetime['hour'],aux_datetime['min'],aux_datetime['sec'])
        aux_run['datetime'] = '%d.%d. %d %02d:%02d:%02d' % (aux_datetime['day'], aux_datetime['month'], int(aux_datetime['year'])+2000, aux_datetime['hour'], aux_datetime['min'], aux_datetime['sec'])                                                                                  
        return aux_run
    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_TERMINAL_INFO"]["cmd"] | 0x80)):
        ''' GET_TERMINAL_INFO RESPONSE
            | number_of_cells (1B) | battery (1B)| backlight (1B) | speaker (1B) | language (1B)
        ''' 
        aux_terminal_info = {}
        aux_time = {}
        
        #if( len(data) == 12):        
        aux_terminal_info['number_of_cells'], aux_terminal_info['battery'], aux_terminal_info['backlight'],  aux_speaker, \
        aux_terminal_info['language'], aux_time['sec'], aux_time['min'], aux_time['hour'], aux_time['day'], aux_time['dayweek'], \
        aux_time['month'], aux_time['year']= struct.unpack("<BBBBBBBBBBBB", data)
#        else:
#            aux_terminal_info['number_of_cells'], aux_terminal_info['battery'], aux_terminal_info['backlight'],  aux_speaker, \
#            aux_terminal_info['language'] = struct.unpack("<BBBBB", data)
        
        aux_terminal_info['speaker'] = {}
        aux_terminal_info['speaker']['keys'] = bool(aux_speaker & 0x01)
        aux_terminal_info['speaker']['system'] = bool(aux_speaker & 0x02)
        aux_terminal_info['speaker']['timing'] = bool(aux_speaker & 0x04)
        aux_terminal_info['backlight'] = bool(aux_terminal_info['backlight'])                
                                
        return aux_terminal_info
    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_TIMING_SETTINGS"]["cmd"] | 0x80)):
        ''' GET_TIMING_SETTINGS RESPONSE
            | timing_logic_mode (1B) | measurement_state (1B)| name_id (1B) | basic_tag_timefilter (1B) |
              lap_timefilter (2B) | lap_numberfilter(1B) | 
        ''' 
        aux_timing_settings = {}
        
        #if( len(data) == 8):        
        aux_timing_settings['logic_mode'], aux_timing_settings['measurement_state'], aux_timing_settings['name_id'],\
        aux_timing_settings['filter_tagtime'], aux_timing_settings['filter_minlaptime'],\
        aux_timing_settings['filter_maxlapnumber'], aux_timing_settings['tags_reading_enable'],\
        = struct.unpack("<BBBBhBB", data)
#        else:                 
#            aux_timing_settings['logic_mode'], aux_timing_settings['measurement_state'], aux_timing_settings['name_id'],\
#            aux_timing_settings['filter_tagtime'],aux_timing_settings['filter_minlaptime'],\
#            aux_timing_settings['filter_maxlapnumber'],\
#            = struct.unpack("<BBBBhB", data)
                
                                                        
        return aux_timing_settings
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_DIAGNOSTIC"]["cmd"] | 0x80)):
        ''' GET_DIAGNOSTIC RESPONSE
            | nr1 (1B) | nr2 (1B)| .. | nrx (1B) | 
        ''' 
        aux_diagnostic = {}
        
        #values = struct.unpack('<bb', senddata) #[3,0, .. 5]         
        
        values = struct.unpack('<'+len(data)*'b', data) #[3,0, .. 5]
        keys = ['nr{0}'.format(x) for x in range(1, len(values)+1)] #['nr1','nr2' .. 'nr3']
        aux_diagnostic = dict(zip(keys, values))
        
        return aux_diagnostic                       
        
        
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_SPEAKER"]["cmd"] | 0x80)):        
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_BACKLIGHT"]["cmd"] | 0x80)):        
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_TIMING_SETTINGS"]["cmd"] | 0x80)):        
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["ENABLE_START_CELL"]["cmd"] | 0x80)):        
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["ENABLE_FINISH_CELL"]["cmd"] | 0x80)):        
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["QUIT_TIMING"]["cmd"] | 0x80)):        
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GENERATE_STARTTIME"]["cmd"] | 0x80)):        
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GENERATE_FINISHTIME"]["cmd"] | 0x80)):        
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["CLEAR_DATABASE"]["cmd"] | 0x80)):        
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_TAGS_READING"]["cmd"] | 0x80)):        
        return data    
    else:
        for cmd_string, cmd_nr in DEF_COMMANDS.DEF_ERRORS.items():
            if(command == cmd_nr):
                print "E: callback: cmd:", cmd_nr, cmd_string

    print "E: callback: cmd: " + str(command) +","+ data
    return {'error':command} 

def pack_data(command_key, data):
    
    """ pack data for sending (from dict or number to string) """
    
    command = DEF_COMMANDS.DEF_COMMANDS[command_key]['cmd']
    length = DEF_COMMANDS.DEF_COMMANDS[command_key]['length']    
    
    #print "pack data: ", command, data, type(data)
    if(command == DEF_COMMANDS.DEF_COMMANDS["SET_SPEAKER"]['cmd']):        
        # SET SPEAKER
        aux_data = struct.pack('BBB',int(data["keys"]), int(data["timing"]), int(data["system"]))
                                                                                         
    elif(command == DEF_COMMANDS.DEF_COMMANDS["SET_TIMING_SETTINGS"]['cmd']):        
        # SET TIMING SETTINGS
        aux_data = struct.pack('<BBBhB', data['logic_mode'], data['name_id'], data['filter_tagtime'],\
                               data['filter_minlaptime'], data['filter_maxlapnumber'])        
    elif(command == DEF_COMMANDS.DEF_COMMANDS["GET_DIAGNOSTIC"]['cmd']):        
        # GET DIAGNOSTIC        
        aux_data = struct.pack('<BB', data['start'], data['count'])
        
    # NUMBER    
    elif(length == 1):
        aux_data = struct.pack('B', data)
    elif(length == 2):
        aux_data = struct.pack('H', data)
    elif(length == 4):
        aux_data = struct.pack('L', data)
    else:
        aux_data = data
        
    return aux_data

        
       
    