# -*- coding: utf-8 -*-

'''
Created on 16.9.2009
@author: Luboš Melichar

  desc: UART protocol for application-terminal communication
  application counts as MASTER, terminal counts as SLAVE
  communication session can be initiated only by MASTER
  MASTER starts by sending command
  ------------------------------------------------------------
  | STARTBYTE | SEQ | COMMAND | DATALENGTH | DATA | .. | XOR |
  ------------------------------------------------------------
  STARTBYTE = 0x53 (byte), constant for start of frame
  SEQ = 0-255(byte), control id of command in case of retransmit
  COMMAND = 0-0x7F(byte), application command
          = 0-0x7F+0x80(byte), terminal acknowledge for good received command
  DATALENGTH = 0-255(byte), length of transmitted data
  DATA = payload, contains useful info
  XOR = 0-0xFF(byte), logic xor of STARTBYTE, SEQ, COMMAND, DATALENGTH and DATA (if any)
 
  SLAVE executes command (using function comm_app_process()) and
  responds with the equal structured frame, but the COMMAND MSb is
  set to 1
 
 Commands
     CMD_GET_RUN_PAR_INDEX         0x30
     CMD_GET_TIME_PAR_INDEX        0x32


'''

import serial, time
import binascii
import sqlite3
from struct import unpack
import _winreg as winreg
import re, itertools
#from ewitis.log import log

START_BYTE              =   "\x53"
FRAMELENGTH_NO_DATA     =   5

#protocol states
(eNONE, eWAIT_FOR_STARTBIT, eWAIT_FOR_SEQ, eWAIT_FOR_COMMAND, eWAIT_FOR_DATALENGTH, eWAIT_FOR_DATA, eWAIT_FOR_XOR) = range(0,7)

#exceptions
class Receive_Error(Exception): pass
class SR_SeqNr_Error(Exception): pass
class SendReceiveError(Exception): pass

class SerialProtocol():
    def __init__(self, xcallback, port = None, baudrate = 9600):
        self.callback = xcallback
        self.port = port
        self.baudrate = baudrate        
        self.seq_id = 1            
        
    def xor(self, string):
        xor = 0        
        for i in range(len(string)):            
            xor ^= ord(string[i])
        return xor
    
    def open_port(self):
        self.ser = serial.Serial(self.port, self.baudrate)
        '''otevreni portu'''
        if self.ser.isOpen() == 1: #port jiz otevren
            self.ser.close()
        self.ser.open()
        if self.ser.isOpen() == 0:  #port se neotevrel
            print "E: Can not open port:", self.ser.name
            exit
        else:
            print "I: Port is succesfully open:", self.ser.name
            
    def close_port(self):
        '''zavreni portu'''
        self.ser.close()
        if self.ser.isOpen() == 1:  #port se neotevrel
            print "E: Can not close port:", self.ser.name
            exit
        else:
            print "I: Port is succesfully close:", self.ser.name
                       
    #===========================================================================
    # send 1 frame            
    #===========================================================================
    def send_frame(self, cmd, data):
        #self.frame_id = 0x53
        
        aux_string = START_BYTE;
        aux_string += (chr(self.seq_id))
        aux_string += (chr(cmd)) 
        aux_string += chr(len(data))
        aux_string += data        
        aux_string += chr(self.xor(aux_string));
        #print aux_string.encode('hex')
                
        self.ser.write(aux_string)
        #return self.seq_id
        
    #===========================================================================
    # wait for receiving the frame 
    # or comes timeout and set init state
    #===========================================================================
    def receive_frame(self):
                        
        frame = {}
        state = eWAIT_FOR_STARTBIT
        
        #print "buffer:", self.ser.inWaiting(),
        
        #wait for the start bit
        if state == eWAIT_FOR_STARTBIT:
            znak = self.ser.read()            
            while (znak != START_BYTE):
                znak = self.ser.read()
            state = eWAIT_FOR_SEQ
            #print "\n=>eWAIT_FOR_ID",
            
        if state == eWAIT_FOR_SEQ:
            znak = self.ser.read()
            frame['seq_id'] = ord(znak)
            state = eWAIT_FOR_COMMAND
            #print "=>eWAIT_FOR_COMMAND",
            
        if state == eWAIT_FOR_COMMAND:
            znak = self.ser.read()
            frame['cmd'] = ord(znak)
            state = eWAIT_FOR_DATALENGTH
            #print "=>eWAIT_FOR_DATALENGTH",
            
        if state == eWAIT_FOR_DATALENGTH:
            znak = self.ser.read()
            frame['datalength'] = ord(znak)
            state = eWAIT_FOR_DATA
            #print "=>eWAIT_FOR_DATA",
            
        if state == eWAIT_FOR_DATA:
            #cnt = 0
            if(self.ser.inWaiting()<frame['datalength']):
                print"E:NEDOSTATEK DAT! (cekam..)"
            #else:
            frame['data'] = self.ser.read(frame['datalength'])
            state = eWAIT_FOR_XOR
            #print "=>eWAIT_FOR_XOR",
            
        if state == eWAIT_FOR_XOR:            
            znak = self.ser.read()            
            #callback_return = self.callback(frame['cmd'], frame['data'])
            state = eWAIT_FOR_STARTBIT
            return frame
        raise Receive_Error()
    
    #=======================================================================
    # - vyslani cmd + data
    # - prijmuti odpovedi
    # - zavolani callbacku(cmd, data) a vraceni jiz slovniku s konkretnimi daty
    #=======================================================================
    def send_receive_frame(self, cmd, data):
        
        '''clear buffers'''
        self.ser.flushInput()
        self.ser.flushOutput()
        
        
        for attempt in range(3):
            
            '''increment sequence id'''
            self.seq_id += 1
            self.seq_id &= 0xFF
        
            '''send frame'''
            self.send_frame(cmd, data)            
            
            '''wait for enough data'''
            for attempt_2 in range(5):                
                if(self.ser.inWaiting() >= len(data) + FRAMELENGTH_NO_DATA):
                    break                
                time.sleep(0.1)
            else:
                continue #no enough data, try send,receive again
            
            '''receive answer'''
            try:                                   
                aux_frame = self.receive_frame()
                if(aux_frame['seq_id'] != self.seq_id):
                    raise SendReceiveError(1, "no match sequence ids")
                
                '''ALL OK'''
                break   #end of for
            except (Receive_Error, SendReceiveError) as (errno, strerror):
                print "W:SendReceiveError - {1}({0}) , try again..".format(errno, strerror)
                                                  
        else:                       
            raise SendReceiveError(100,"no valid response")
            
            
                                        
        '''call user callback to parse data to dict structure'''
        aux_dict = self.callback(aux_frame['cmd'], aux_frame['data'])
        
        '''ADD COMMON data and errors'''
        
        '''common errors'''
        #aux_dict['common_errors'] = 0

        
        return aux_dict
        
                
if __name__ == "__main__":
    
    import struct
    import libs.file.file as file
    
    def funkce_callback(command, data):
        print "\nCallback=> cmd:", hex(command), "data", data.encode('hex')             
        if(command == CMD_GET_RUN_PAR_INDEX):
            return "get time"
        
        elif(command == (CMD_GET_TIME_PAR_INDEX | 0x80)):
            ''' GET_TIME_PAR_IDNEX => RUN struct (16b) + 2b error
                | error (2b) | state(1b) | id (4b) | run_id (2b) | user_id (4b) | cell (1b) | time(4b) |
            '''                                          
            aux_run = {}        
            aux_run['error'], aux_run['state'], aux_run['id'],  aux_run['run_id'], \
            aux_run['user_id'], aux_run['cell'], aux_run['time'], = struct.unpack("<HBIHIBI", data)                        
                           
            return aux_run
        return "error"      

    csv_export_file = file.File("export.csv")    
    
    protokol = SerialProtocol( funkce_callback, port='COM8', baudrate=38400)
    
    
    try:        
        protokol.open_port()
    except serial.SerialException:
        print "Port se nepodařilo otevřít"
    else:       
        index = 0x00        
        aux_csv_string = "state;index;id;time\n"
        csv_export_file.add(aux_csv_string)
            
        while(1):              
            time.sleep(1)
            
            ''' send request and receive run record '''
            try:                    
                run = protokol.send_receive_frame(CMD_GET_TIME_PAR_INDEX, chr(index)+"\x00")
            except sqlite3.IntegrityError:                
                raise
                        
            
            if(run['error'] == 0):               
                aux_csv_string = str(run['state']) + ";" + str(index) + ";" + str(run['id']) + ";" + str(run['time'])
                print "I:receive run: " + aux_csv_string                 
                csv_export_file.add(aux_csv_string)   
                index += 1                                            
            else:
                print "no new run"

 
                    
                