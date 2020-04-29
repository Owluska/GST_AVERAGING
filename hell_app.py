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
import matplotlib.pyplot as plt
import random
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

ports=list(lp.comports())
for p in ports:
    print(p)
    
# try:    
#     com = serial.Serial('COM3', baudrate=115200, timeout=0.02)

# except Exception:
#     serial.Serial('COM3').close()

# def initPort(name, baudrate):
#     serial.Serial() as com:
#   #   with serial.Serial() as com:
#         com.port=name
#         com.baudrate=baudrate
#         # com.timeout=timeout
#         if com.isOpen():
#             com.close()
#         else:
#             try:
#                 com.open()
#             except(OSError, serial.SerialException):
#                 pass
#         return com



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

def get_arrays(com, cmd="last_angles:data\r"):
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


def prep_angles(arr):
    arr = ap.scan_n_complete(arr, end_symbol='\n') 
    arr= [s[:-2] for s in arr]
    series=pd.Series(arr, dtype=float, name='name')
    return series
    
#com3=initPort('COM3', 115200)
com3 = serial.Serial('COM3', baudrate=115200, timeout=0.02)
start_measurments(com3)

just_angles=get_arrays(com3, cmd="just_angles:data\r")
sma_angles=get_arrays(com3, cmd="sma_angles:data\r")
kwma_angles=get_arrays(com3, cmd="_wma_angles:data\r")
last_angles=get_arrays(com3, cmd="last_angles:data\r")
       

com3.close()

names=['indexes','just_angles', 'sma_angles', 'kwma_angles', 'last_angles']
# angles=[just_angles, sma_angles, _wma_angles, last_angles]

# for a,nm in zip(angles, names):
    
#     a=ap.scan_n_complete(a, end_symbol='\n')
#     print(a)
#     a= [s[:-2] for s in a]
#     a=pd.Series(a, dtype=float, name=nm)


ja_s=prep_angles(just_angles)
sma_s=prep_angles(sma_angles)
kwma_s=prep_angles(kwma_angles)
la_s=prep_angles(last_angles)

x=pd.Series([i for i in just_angles], name='indexes')
data = [x, ja_s, sma_s, kwma_s, la_s]
frame = {nm:dt for nm, dt in zip(names, data)}

averagings = pd.DataFrame(frame)

y_cols=averagings.columns[1:]
x_col=x.name

# ax=plt.gca()
# plt.figure(figsize=(20,20))
fig, ax = plt.subplots(figsize=(20,20))

for y_col in y_cols:    
    averagings.plot(kind='line', x=x_col, y=y_col, ax=ax)
    

ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))


ax.xaxis.set_minor_locator(MultipleLocator(0.5))


ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))


ax.yaxis.set_minor_locator(MultipleLocator(0.5))


ax.xaxis.grid(True, which='both')
ax.yaxis.grid(True, which='both')

#plt.legend(y_cols)
plt.show()

a = random.randrange(100)
path ='data/result_rn{:d}.png'.format(a)
fig.savefig(path)
