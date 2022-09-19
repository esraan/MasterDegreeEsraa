#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 12:23:51 2019

@author: esraan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 13:42:09 2019

@author: esraan
"""

import pandas as pd 
import numpy as np
from scipy import stats
import math
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
res= {}
resfreq = {}
resall = {}
excel_file_name = str(input ('Enter your excel fila name:'))
sheet = pd.read_excel(excel_file_name)
data_head = list(sheet.columns)
lowlimit = float(input("Enter your lowlimit value: ") )
highlimit = float(input("Enter your highlimit value: ") )
bin_width = float(input("Enter your bins width value: ") )
#list_use =list(np.linspace(lowlimit,highlimit,bin_num))
list_use =list(np.arange(lowlimit,highlimit,bin_width))
list_use.append(highlimit)
print(list_use)
daisy = []
for head in data_head:
    x = sheet[head].dropna().count()
    #mini = sheet[head].dropna().min()
    #maxi = sheet[head].dropna().max()
    for i in range(len(list_use)):
        if i == 0:
            resfreq['<%.2E' % Decimal(list_use[i])] = sheet[head][sheet[head]<list_use[i]].count()/x 
            if '<%.2E' % Decimal(list_use[i]) not in daisy:
                daisy.append('<%.2E' % Decimal(list_use[i]))
        elif i == len(list_use)-1:
            resfreq['%.2E' % Decimal(list_use[i-1])+'-'+ '%.2E' % Decimal(list_use[i])] = sheet[head][(sheet[head]<list_use[i]) & (sheet[head]>list_use[i-1])].count()/x
            if '%.2E' % Decimal(list_use[i-1])+'-'+ '%.2E' % Decimal(list_use[i]) not in daisy:
                daisy.append('%.2E' % Decimal(list_use[i-1])+'-'+ '%.2E' % Decimal(list_use[i]))
            resfreq['>%.2E' % Decimal(list_use[i])] = sheet[head][sheet[head]>list_use[i]].count()/x
            if '>%.2E' % Decimal(list_use[i]) not in daisy:
                daisy.append('>%.2E' % Decimal(list_use[i]))
        else:
            resfreq['%.2E' % Decimal(list_use[i-1])+'-'+ '%.2E' % Decimal(list_use[i])] = sheet[head][(sheet[head]<list_use[i]) & (sheet[head]>list_use[i-1])].count()/x
            if '%.2E' % Decimal(list_use[i-1])+'-'+ '%.2E' % Decimal(list_use[i]) not in daisy:
                daisy.append('%.2E' % Decimal(list_use[i-1])+'-'+ '%.2E' % Decimal(list_use[i]))
    resall[head] = resfreq.copy()




day = pd.DataFrame(resall)
day['order'] = pd.Categorical(day.index , categories=daisy, ordered=True)
day.sort_values('order',inplace=True)


day = day.drop(['order'], axis = 1)
day.to_excel('file.xlsx')
new = pd.melt(day)

plt.figure(figsize=(15, 10))
c = daisy * len(data_head)
new ['cluster area size'] = c
new.columns = ['consturcts','relative frequancy','cluster area size']
svm = sns.barplot(x= 'cluster area size', hue='consturcts', y='relative frequancy', data=new)
plt.show()

figure = svm.get_figure()    
figure.savefig('output.png', dpi=700)
