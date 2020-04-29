# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 18:10:26 2020

@author: Ксения
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

path='averaging.xlsx'
#names = ['ema_angles', 'nsf_angles', 'last_angles', '_wma_angles', 'wma_angles', 'sma_angles', 'just_angles']
averagings=pd.read_excel(path, dtype = np.float64)

# cols = averagings.columns
# for col in cols:
#     if col[-1] ==';':
#         col=col[:-1]
#         print(col)

# cols

#print(averagings.head())

x=pd.Series([row for row in averagings.index], name='indexes')
averagings.insert(0, 'indexes', x)
#print(y)

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
plt.show()

fig.savefig('result.png')

