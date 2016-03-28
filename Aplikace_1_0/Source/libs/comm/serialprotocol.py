# -*- coding: utf-8 -*-
#Created on 16.9.2009
#author: Luboš Melichar

"""
Serialprotocol Module
**********************
    UART protocol for application-terminal communication
    application counts as MASTER, terminal counts as SLAVE
    communication session can be initiated only by MASTER
    MASTER starts by sending command
    
    SLAVE executes command (using function comm_app_process()) and
    responds with the equal structured frame, but the COMMAND MSb is
    set to 1

Frame
+++++
    
    +-----------+-----+---------+------------+----------+-----+
    | STARTBYTE | SEQ | COMMAND | DATALENGTH |   DATA   | XOR |
    +===========+=====+=========+============+==========+=====+
    |    1B     | 1B  |    1B   |    1B      |    0-64B |  0  |
    +-----------+-----+---------+------------+----------+-----+
    
    ::
    
        STARTBYTE = 0x53 (byte), constant for start of frame
        SEQ = 0-255(byte), control id of command in case of retransmit
        COMMAND = 0-0x7F(byte), application command
        COMMAND = 0-0x7F+0x80(byte), terminal acknowledge for good received command
        DATALENGTH = 0-255(byte), length of transmitted data
        DATA = payload, contains useful info
        
    SLAVE executes command (using function comm_app_process()) and
    responds with the equal structured frame, but the COMMAND MSb is
    set to 1       
"""

import serial, time
import binascii
#import sqlite3
import pysqlite2
import struct
import _winreg as winreg
import re, itertools
import ewitis.comm.DEF_COMMANDS as DEF_COMMANDS
#from ewitis.log import log

#: start byte constant
START_BYTE              =   "\x53"
FRAMELENGTH_NO_DATA     =   5

#protocol states
(eNONE, eWAIT_FOR_STARTBIT, eWAIT_FOR_SEQ, eWAIT_FOR_COMMAND, eWAIT_FOR_DATALENGTH, eWAIT_FOR_DATA, eWAIT_FOR_XOR) = range(0,7)

#exceptions
class Receive_Error(Exception): pass
class SendReceiveError(Exception): pass
#class SR_SeqNr_Error(Exception): pass

class SerialProtocol():
    """    
    """
    
    def __init__(self, port = None, baudrate = 9600):

        self.port = port
        self.baudrate = baudrate        
        self.seq_id = 1                    
        
    def xor(self, string, init = 0):
        """checksumm"""
        xor = init        
        for i in range(len(string)):            
            xor ^= ord(string[i])
        return xor
    
    def open_port(self):
        """
        otevře port
          
        *toDo:*
          při neúspěšném otevření, vyhodit vyjímku
        """
                
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
        """
        zavře port        
                
        *toDo:*
          při neúspěšném zavření, vyhodit vyjímku
        
        """
        
        self.ser.close()
        if self.ser.isOpen() == 1:  #port se neotevrel
            print "E: Can not close port:", self.ser.name
            exit
        else:
            print "I: Port is succesfully close:", self.ser.name

    def send_frame(self, command, data):
        """
        poskládá a odesílá jeden frame      
        
        *parameters:*
          command: a
          
          data: byte, short integer, integer, string
        """    

        aux_string = START_BYTE;
        aux_string += (chr(self.seq_id))
        aux_string += (chr(command)) 
        aux_string += chr(len(data))
        aux_string += data        
        aux_string += chr(self.xor(aux_string));
                               
        self.ser.write(aux_string)        
        #return self.seq_id


    def receive_frame (self):
        """
        přijme jeden frame,
       
        *return:*
          poskládaný frame                 
       
        """
                       
        frame = {}                     
        znak = ''                  

        #1. start byte
        while (znak != START_BYTE):
            znak = self.ser.read()
            if len(znak) == 0:
                raise Receive_Error(1, "timeout: no start byte" ) #timeout, no start byte in stream
        xor = self.xor(znak)        
                                           
        #2.byte - sequence       
        znak = self.ser.read()
        if len(znak) == 0:
            raise Receive_Error(2, "timeout: no sequence" ) #timeout, no sequence byte
        xor = self.xor(znak, xor)           
        frame[ 'seq_id'] = ord(znak)
           
        #3.byte - command       
        znak = self.ser.read()
        if len(znak) == 0:
            raise Receive_Error(3, "timeout: no command" ) #timeout, no command
        xor = self.xor(znak, xor)
        frame[ 'cmd'] = ord(znak)
                   
        #4.byte - data length           
        znak = self.ser.read()
        if len(znak) == 0:
            raise Receive_Error(4, "timeout: no data length" ) #timeout, length
        xor = self.xor(znak, xor)
        frame[ 'datalength'] = ord(znak)                   
                                                     
        #5.byte - data
        if( self.ser.inWaiting() < frame['datalength' ]):
            print"E: NEDOSTATEK DAT! (cekam..)"            
        frame[ 'data'] = self .ser.read(frame['datalength'])       
        if len(frame[ 'data']) != frame[ 'datalength']:
            raise Receive_Error(5, "timeout: no enough data" ) #timeout, no enough data
        xor = self.xor(frame[ 'data'], xor)                           
           
        #last byte - xor                   
        znak = self.ser.read()
        if len(znak) == 0:
            raise Receive_Error(6, "timeout: no checksum" ) #timeout, no xor
       
        #calc xor
        if ord(znak) != xor:            
            raise Receive_Error(10, "timeout: no valid checksum" ) #timeout, wrong xor
                   
        #return frame                  
        return frame 

    
    
    def send_receive_frame(self, cmd, data):        
        """
        1. vyšle frame
        2. počká na dostatek dat
        3. přijme odpověď
        4. zavolá callback(command, data)
        5. vrací slovník s rozparsovanými daty 
        
        *return:*
            dict{}        
        *toDo:*
            při čekání na odpověď se nějak komicky na počet bajtů..
            self.ser.inWaiting() >= len(data) + FRAMELENGTH_NO_DATA
        """                
        
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
                time.sleep(0.03)               
                if(self.ser.inWaiting() >=  FRAMELENGTH_NO_DATA):
                    break                                          
            else:
                print "E: no enought data"
                continue #no enough data, try send,receive again
                        
            time.sleep(0.01)
            
            '''receive answer'''
            try:                                 
                aux_frame = self.receive_frame()
                #aux_frame = self.receive_frame_old()
                if(aux_frame['seq_id'] != self.seq_id):                                        
                    raise SendReceiveError(1, "no match sequence ids")
                
                '''ALL OK'''
                break   #end of for
            except (Receive_Error, SendReceiveError) as (errno, strerror):
                print "E:SendReceiveError - {1}({0}) , try again..".format(errno, strerror)
                                                  
        else:                       
            raise SendReceiveError(100,"no valid response")                                                                                
                
        return aux_frame
        
                
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
            #except sqlite3.IntegrityError:
            except pysqlite2.dbapi2.IntegrityError:                
                raise
                        
            
            if(run['error'] == 0):               
                aux_csv_string = str(run['state']) + ";" + str(index) + ";" + str(run['id']) + ";" + str(run['time'])
                print "I:receive run: " + aux_csv_string                 
                csv_export_file.add(aux_csv_string)   
                index += 1                                            
            else:
                print "no new run"

 
                    
                