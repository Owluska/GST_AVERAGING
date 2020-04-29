# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:28:23 2020

@author: Ксения
"""
# import time
# import pandas as pd

# a= ['100.759\r\n', '71.324\r\n', '71.92\r\n', '71.195\r\n',
#  '71.324\r\n', '71.324','\r\n', '80', '.', '651', '\r', '\n'] 

# a= ['100.759','\r\n', '71','.324\r\n', '71.92\r\n', '71.195\r\n',
#   '71.324\r\n', '71.324','\r\n', '80', '.', '651', '\r', '\n'] 

def scan_n_complete(arr, end_symbol='\n'):
    asize=(len(arr)) 
    new_arr=[]       
    skip = 0
    
    for s,n in zip(arr,range(asize)):
        if skip != 0:
            skip=skip-1
            continue
        cr = s.find(end_symbol)
        if cr >= 0:
            new_arr.append(arr[n])
            continue
        else:
            k=n+1
            ts = s
            while(k < (asize)):
                cr = arr[k].find(end_symbol)
                ts=ts+str(arr[k])
                k=k+1        
                if cr >= 0:
                    new_arr.append(ts)
                    skip=(k-n)-1
                    break    
    return new_arr


# b = scan_n_complete(a, end_symbol='\n') 
# b= [s[:-2] for s in b]
# series=pd.Series(b, dtype=float, name='name')      
# print(b)
