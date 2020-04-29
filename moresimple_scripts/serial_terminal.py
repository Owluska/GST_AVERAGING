# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 18:10:26 2020

@author: Ксения
"""


import serial.tools.list_ports as lp
import serial
#import time
import array_parsing as ap
import pandas as pd

ports=list(lp.comports())
for p in ports:
    print(p)
    
try:    
    com = serial.Serial('COM3', baudrate=115200, timeout=0.02)

except Exception:
    serial.Serial('COM3').close()
#    print('e')
#    com = serial.Serial('COM3', baudrate=115200, timeout=0.02)

# com = serial.Serial('COM3', baudrate=115200, timeout=0.02)


def start_measurments(com):    

    write_data="fil_test:start\r".encode('utf-8')
    com.write(write_data)
    stop = False 
    while(stop!=True):
          
        if com.inWaiting!=0:
            read_data=com.readlines()
            for rd in read_data:
                if stop:
                    break
                rd = rd.decode('utf-8')
                print(rd,end='')
                words = rd.split()
                for w in words:
                    #print(w)
                    if w == 'Ended':
                        stop = True
                        break

def get_arrays(cmd="last_angles:data\r", com=com):
    array=[]
    write_data=cmd.encode('utf-8')
    com.write(write_data)
    condition = False
    while(condition != True):          
        if com.inWaiting!=0:
            read_data=com.readlines()
            if(read_data != []):
                for rd in read_data:
                    rd = rd.decode('utf-8')
                    if ((rd !="start\r\n") and (rd !="stop\r\n")):
                        array.append(rd)
                    if rd == "stop\r\n":
                        condition = True
                        break 
    return array


   

start_measurments(com)

just_angles=get_arrays(cmd="just_angles:data\r", com=com)
sma_angles=get_arrays(cmd="sma_angles:data\r", com=com)
_wma_angles=get_arrays(cmd="_wma_angles:data\r", com=com)
last_angles=get_arrays(cmd="last_angles:data\r", com=com)
       

com.close()
names=['indexes','just_angles', '_sma_angles', '_wma_angles', 'last_angles']
angles=[]
just_angles=ap.scan_n_complete(just_angles)
just_angles= [s[:-2] for s in just_angles]
jas=pd.Series(just_angles, dtype=float, name='just_angles') 



