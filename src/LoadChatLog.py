# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 23:33:06 2018

@author: Joowhan Song
"""

import glob
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from operator import itemgetter

#%%

chatLogName = glob.glob('..\\data\\*.txt')

timeFmt = '%H:%M:%S.%f'

timeStamps = list()
userIDs = list()
chats = list()

maxIdxNum = 5

# %%
with open(chatLogName[0], 'r', encoding='utf-8') as chatLog:
    for i, line in enumerate(chatLog):
        timeStr = line[line.find('[') + 1:line.find(']')]
        time = (datetime.strptime(timeStr, timeFmt) - datetime(1900,1,1)).total_seconds()
        # time = datetime.strptime(timeStr, timeFmt)
        
        chatStr = line[line.find(']') + 2:]
        userID = chatStr[:chatStr.find(':')]
        chat = chatStr[chatStr.find(':') + 1:chatStr.find('\n')]

        timeStamps.append(time)
        userIDs.append(userID)
        chats.append(chat)

# %%
plt.figure()
chatNum = np.asarray(range(1, len(timeStamps) + 1))
plt.plot(timeStamps, chatNum)

#%%
plt.figure(figsize=(12, 12))
chatHist = plt.hist(timeStamps, bins=np.int(timeStamps[-1] / 60))
plt.ylabel('Number of Chats')
plt.xlabel('Time(seconds)')

#%%

chatHistIndex = np.asarray(range(0, len(chatHist[0])))
chatHistSum = np.cumsum(chatHist[0])

#%%
plt.plot(chatHist[0])

#%%
chatTable = np.stack([chatHist[0], chatHistIndex], axis=1)

#%%
chatTableSorted = np.asarray(sorted(chatTable, key = itemgetter(0), reverse=True))

#%%

maxIdx = list()

for i in range(0, maxIdxNum):
    maxIdx.append(int(chatTableSorted[i, 1]))

#%%

underBound = list()
upperBound = list()

for i in range(0, maxIdxNum):
    underBound.append(chatHist[1][maxIdx[i]])
    upperBound.append(chatHist[1][maxIdx[i] + 1])

#%%
hotChats = list()

for i in range(0, maxIdxNum):
    booleanIdx = np.array((timeStamps > underBound[i]) & (timeStamps < upperBound[i]))
    hotChat = np.asarray(chats)[booleanIdx]
    hotChats.append(hotChat)
    
#%%
hotChats[4]

        