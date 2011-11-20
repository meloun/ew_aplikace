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

#===============================================================================
# COMMANDS
#===============================================================================
CMD_GET_RUN_PAR_INDEX   =   0x30
CMD_GET_TIME_PAR_INDEX  =   0x32

#===============================================================================
# CALLBACK
#===============================================================================
def callback(command, data):
    #print "\nCallback=> cmd:", hex(command), "data", data.encode('hex')             
    if(command == CMD_GET_RUN_PAR_INDEX):
        return "get time"
    
    # GET TIME PAR INDEX
    elif(command == (CMD_GET_TIME_PAR_INDEX | 0x80)):
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
    elif(command == (CMD_GET_RUN_PAR_INDEX | 0x80)):        
        ''' GET_RUN_PAR_IDNEX => RUN struct (16b) + 2b error
            | error (2b) | state(1b) | id (4b) | starttime_id (4b) | datetime (6b) | name_id (1b) 
        '''                                          
        aux_run = {}
        aux_datetime = {}        
        aux_run['error'], aux_run['state'], aux_run['id'],  aux_run['starttime_id'], \
        aux_datetime['sec'], aux_datetime['min'],aux_datetime['hour'],aux_datetime['day'],aux_datetime['month'],aux_datetime['year'],\
        aux_run['name_id'] = struct.unpack("<HBIIBBBBBBB", data)
        
        #add data      
        #aux_run['datetime'] =  '{0}.{1} {2}  {3}:{4}:{5}'.format(aux_datetime['day'], aux_datetime['month'], int(aux_datetime['year'])+2000,aux_datetime['hour'],aux_datetime['min'],aux_datetime['sec'])
        aux_run['datetime'] = '%d.%d %d %02d:%02d:%02d' % (aux_datetime['day'], aux_datetime['month'], int(aux_datetime['year'])+2000,aux_datetime['hour'],aux_datetime['min'],aux_datetime['sec'])                                                                                  
        return aux_run
    return "E: callback error" 
