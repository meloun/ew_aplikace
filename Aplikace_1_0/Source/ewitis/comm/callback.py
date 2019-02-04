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
    
    #print "callback", hex(command-0x80) if command>0x80 else hex(command), data.encode('hex'), len(data)

    #error check
    if command <= 0x80:        
        for cmd_string, cmd_nr in DEF_COMMANDS.DEF_ERRORS.items():
            if(command == cmd_nr):
                print "E: comm: error", command, cmd_string, data            
        return {'error':command}
        
    # rx length check
    def_command = DEF_COMMANDS.GetParCmd(command-0x80)
    if (def_command[1]['length-rx'] != 255) and (def_command == None or def_command[1]['length-rx'] != len(data)):        
        print "E: comm: wrong length", len(data), def_command[1]['length-rx'], "command:", command
        return {'error':command}

    # HW & FW VERSIONS
    if(command == (DEF_COMMANDS.DEF_COMMANDS["GET_HW_SW_VERSION"]["cmd"] | 0x80)):
        aux_versions = {}
        aux_versions['hw1'], aux_versions['hw2'],aux_versions['hw3'], aux_versions['fw1'],  aux_versions['fw2'], aux_versions['fw3']\
        = struct.unpack("<cc2scc2s", data)

        #some sugar
        if aux_versions['hw1']== 'B':
            aux_versions['hw1'] = 'Blackbox'
        else:
            aux_versions['hw1'] = 'Terminal'
        if aux_versions['fw1']== 'I':
            aux_versions['fw1'] = 'IR'
        else:
            aux_versions['fw1'] = 'RFID'

        #    
        aux_versions = {"hw": aux_versions['hw1']+' '+aux_versions['hw2']+'.'+aux_versions['hw3'],
                        "fw": aux_versions['fw1']+' '+aux_versions['fw2']+'.'+aux_versions['fw3'],
                        "device": aux_versions['hw1']+'-'+aux_versions['fw1']
                        }
        print aux_versions
        return aux_versions


    # GET TIME PAR INDEX
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_TIME_PAR_INDEX"]["cmd"] | 0x80)):
        ''' GET_TIME_PAR_IDNEX => TIME struct (16b) + 2b error
            | error (2b) | state(1b) | id (4b) | run_id (2b) | user_id (4b) | cell (1b) | time(4b) |
        '''
        aux_time = {}
        aux_not_used = 0
        
        aux_time['error'], aux_not_used, aux_time['id'],  aux_state, \
        aux_not_used, aux_time['cell'],aux_time['time_raw'], = struct.unpack("<HBIHIBI", data)

        aux_time['user_id'] = 0;
        
        #time on request
        aux_time['state'] = "---"
        if (aux_state & 0x01) == 0x01:
            aux_time['state'] = aux_time['state'][0] + "R" + aux_time['state'][2]            
                
        #manual time
        if (aux_state & 0x02) == 0x02:
            aux_time['state'] = aux_time['state'][0] + aux_time['state'][1] + "M"
                 
        #pricteni casu ke vsem casum, chyba blizak
        #if(aux_time['cell'] != 1):
        #    aux_time['time_raw'] = aux_time['time_raw'] + 255800

        #add data
        #aux_time['time1'] = None        

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

        return aux_terminal_info

    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_DEVICE_OVERVIEW"]["cmd"] | 0x80)):
        ''' GET_DEVICE_OVERVIEW RESPONSE
            | actual race time (4B) | measurement state (1B)| tag reading (1B) | reseved (10B)
        ''' 
        aux_terminal_overview = {}
        r = ""

        aux_terminal_overview['race_time'], aux_terminal_overview['measurement_state'], aux_terminal_overview['autoenable_cell'],\
        r, r, r, r, r, r, r, r, r, r \
        = struct.unpack("<IBBBBBBBBBBBB", data)

        return aux_terminal_overview

    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_TIMING_SETTINGS"]["cmd"] | 0x80)):
        ''' GET_TIMING_SETTINGS RESPONSE
            | timing_logic_mode (1B) | measurement_state (1B)| name_id (1B) | basic_tag_timefilter (1B) |
              lap_timefilter (2B) | lap_numberfilter(1B) | 
        '''
        aux_timing_settings = {}
             
        aux_timing_settings['logic_mode'], aux_timing_settings['measurement_state'], aux_timing_settings['times_download_mode'],\
        aux_timing_settings['autoenable_cell'], aux_timing_settings['autoenable_bb'],\
        aux_timing_settings['autorequest_missingtimes'], aux_timing_settings['tags_reading_enable'],\
        = struct.unpack("<BBBBhBB", data)

        return aux_timing_settings

    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_CELL_INFO"]["cmd"] | 0x80)):
        ''' GET_CELL_INFO
            | battery (1B) | flags (1B)| address (1B) | task (1B) |
             diagnostic_long_ok (2B) | diagnostic_long_ko(2B) | diagnostic_short_ok (1B) | diagnostic_short_ko(1B) | 
        '''
        aux_cell_info = {}

        aux_cell_info['battery'], aux_flags, aux_cell_info['address'],\
        aux_cell_info['task'], aux_cell_info['diagnostic_long_ok'], aux_cell_info['diagnostic_long_ko'],\
        aux_cell_info['diagnostic_short_ok'], aux_cell_info['diagnostic_short_ko'],\
        aux_flags2, aux_cell_info['times_bb'], aux_cell_info['times_cell'], aux_cell_info['fu2']\
        = struct.unpack("<BBBBhhBBBhhh", data)

        #flags
        aux_cell_info['ir_signal'] = bool(aux_flags & 0x01)
        aux_cell_info['synchronized_once'] = bool(aux_flags & 0x02)
        aux_cell_info['synchronized'] = bool(aux_flags & 0x04)
        aux_cell_info['active'] = bool(aux_flags & 0x80)
        #print "f",aux_flags

        aux_cell_info['trigger'] = (aux_flags2 & 0x07)
        aux_cell_info['auto_enable'] = (aux_flags2 >> 3) & 0x07
        aux_cell_info['missing_time_flag'] = (aux_flags2 >> 6) & 0x03
        
        return aux_cell_info

    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_CELL_OVERVIEW"]["cmd"] | 0x80)):
        ''' GET_CELL_OVERVIEW
            | cell1 (1B) | cell2 (1B)| .. | cell14 (1B) |            
            byte - | ir(1b) | synced once (1b) | synced (1b) | not used (4b) | active (1b)            
        '''

        #        
        aux_cell_flags = [None,]*len(data)
        aux_cell_overview = [{}]*len(data)

        aux_cell_flags[0],  aux_cell_flags[1],  aux_cell_flags[2],  aux_cell_flags[3],\
        aux_cell_flags[4],  aux_cell_flags[5],  aux_cell_flags[6],  aux_cell_flags[7],\
        aux_cell_flags[8],  aux_cell_flags[9],  aux_cell_flags[10], aux_cell_flags[11],\
        aux_cell_flags[12], aux_cell_flags[13], aux_cell_flags[14], aux_cell_flags[15],\
        aux_cell_flags[16], aux_cell_flags[17], aux_cell_flags[18], aux_cell_flags[19],\
        aux_cell_flags[20], aux_cell_flags[21], aux_cell_flags[22], aux_cell_flags[23],\
        = struct.unpack("<BBBBBBBBBBBBBBBBBBBBBBBB", data)

        #aux_cell_overview = [{}]*len(data) 
        for i, cell_flags in enumerate(aux_cell_flags):
            
            aux_cell = {}
            aux_cell['ir_signal'] = bool(cell_flags & 0x01)
            aux_cell['synchronized_once'] = bool(cell_flags & 0x02)
            aux_cell['synchronized'] = bool(cell_flags & 0x04)
            aux_cell['missing_time_flag'] = bool(cell_flags & 0x3)
            aux_cell['insystem'] =  bool(cell_flags & 0x40)
            aux_cell['active'] = bool(cell_flags & 0x80)

            aux_cell_overview[i] = aux_cell


        return aux_cell_overview
    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_DIAGNOSTIC"]["cmd"] | 0x80)):
        ''' GET_DIAGNOSTIC RESPONSE
            | nr1 (1B) | nr2 (1B)| .. | nrx (1B) | 
        ''' 
        aux_diagnostic = {}

        senddata = struct.unpack('<bb', senddata) #(0,20)
        values = struct.unpack('<'+len(data)*'b', data) #[3,0, .. 5]
        keys = ['nr{:03d}'.format(x) for x in range(senddata[0], len(values)+senddata[0])]
        descriptions = DEF_COMMANDS.DIAGNOSTICS_DESCRIPTION[senddata[0] : len(values)+senddata[0]]
        aux_diagnostic = dict(zip([str(a) + " : " + b for a,b in zip(keys, descriptions)], values))
        
        return aux_diagnostic
        
        
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_SPEAKER"]["cmd"] | 0x80)):
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_DATETIME"]["cmd"] | 0x80)):
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_TIMING_SETTINGS"]["cmd"] | 0x80)):
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SYNCHRONIZE_SYSTEM"]["cmd"] | 0x80)):
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_CELL_INFO"]["cmd"] | 0x80)):
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_CELL_DIAG_INFO"]["cmd"] | 0x80)):
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["PING_CELL"]["cmd"] | 0x80)):
        return data 
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["RUN_CELL_DIAGNOSTIC"]["cmd"] | 0x80)):
        return data        
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["ENABLE_START_CELL"]["cmd"] | 0x80)):       
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["ENABLE_CELL"]["cmd"] | 0x80)):
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["DISABLE_CELL"]["cmd"] | 0x80)):
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["QUIT_TIMING"]["cmd"] | 0x80)):
        return data
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GENERATE_STARTTIME"]["cmd"] | 0x80)):
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GENERATE_FINISHTIME"]["cmd"] | 0x80)):
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GENERATE_CELLTIME"]["cmd"] | 0x80)):
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["CLEAR_DATABASE"]["cmd"] | 0x80)):
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["SET_TAGS_READING"]["cmd"] | 0x80)):
        return data    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_ACTUAL_RACE_TIME"]["cmd"] | 0x80)):
        aux_time = {}        
        aux_time['time'], = struct.unpack("<I", data)        
        return aux_time    
    elif(command == (DEF_COMMANDS.DEF_COMMANDS["GET_CELL_LAST_TIME"]["cmd"] | 0x80)):
        return data    
    else:
        print "E: comm: unknown command", command
    
    return {'error':command} 

def pack_data(command_key, data):
    
    """ pack data for sending (from dict or number to string) """
    if(type(data)==str):
        return data
    
    command = DEF_COMMANDS.DEF_COMMANDS[command_key]['cmd']
    length_tx = DEF_COMMANDS.DEF_COMMANDS[command_key]['length-tx']
    
    #print "pack data: ", command, data, type(data)
    if(command == DEF_COMMANDS.DEF_COMMANDS["SET_SPEAKER"]['cmd']):
        # SET SPEAKER
        aux_data = struct.pack('BBB',int(data["keys"]), int(data["timing"]), int(data["system"]))
        
    elif(command == DEF_COMMANDS.DEF_COMMANDS["SET_DATETIME"]['cmd']):
        # SET DATETIME        
        aux_data = struct.pack('BBBBBBB', data["second"], data["minute"], data["hour"], data["dayweek"], data["day"], data["month"], data["year"])

    elif(command == DEF_COMMANDS.DEF_COMMANDS["SET_TIMING_SETTINGS"]['cmd']):
        # SET TIMING SETTINGS
        print "TS:", data
        aux_data = struct.pack('<BBBhB', data['logic_mode'], data['times_download_mode'], data['autoenable_cell'],\
                               data['autoenable_bb'], data['autorequest_missingtimes'])
    elif(command == DEF_COMMANDS.DEF_COMMANDS["SET_CELL_INFO"]['cmd']):
        # SET CELL INFO        
        aux_data = struct.pack('<BBBBBB', data['address'], data['task'], data['trigger'],\
                               data['auto_enable'], data['fu1'], data['fu2'])
    elif(command == DEF_COMMANDS.DEF_COMMANDS["SET_CELL_DIAG_INFO"]['cmd']):
        # SET CELL DIAG INFO
        aux_data = struct.pack('<BhhBB', data['address'], data['diagnostic_long_ok'], data['diagnostic_long_ko'],\
                               data['diagnostic_short_ok'], data['diagnostic_short_ko'])
          
    elif(command == DEF_COMMANDS.DEF_COMMANDS["GET_DIAGNOSTIC"]['cmd']):
        # GET DIAGNOSTIC        
        aux_data = struct.pack('<BB', data['start'], data['count'])
#    elif(command == DEF_COMMANDS.DEF_COMMANDS["ENABLE_CELL"]['cmd']):
#        # ENABLE CELL       
#        aux_data = struct.pack('<B', data['task'])
#    elif(command == DEF_COMMANDS.DEF_COMMANDS["DISABLE_CELL"]['cmd']):
#        # DISABLE CELL       
#        aux_data = struct.pack('<B', data['task'])
    elif(command == DEF_COMMANDS.DEF_COMMANDS["GENERATE_CELLTIME"]['cmd']):
        # GENERATE CELLTIME       
        aux_data = struct.pack('<B', data['task'])
        
    # NUMBER    
    elif(length_tx == 1):
        aux_data = struct.pack('B', data)
    elif(length_tx == 2):        
        aux_data = struct.pack('H', data)
    elif(length_tx == 4):
        aux_data = struct.pack('L', data)
    else:
        aux_data = data

    return aux_data

