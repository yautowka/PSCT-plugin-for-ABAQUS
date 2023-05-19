# -*- coding: utf-8 -*-
"""
Created on Sun May 14 10:02:29 2023

@author: LabPC_807
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def get_data_for_graph(path, files, num):
  PEEQ = []
  Rf2 = []
  for file in files:
    if num == 0:
        break
    rf = np.loadtxt(path+'/'+file,dtype='double',skiprows=22,max_rows=1)[8]
    Rf2.append(abs(rf)/1000000)
    #print(time)
    data = np.loadtxt(path+'/'+file,dtype='double',skiprows=44)
    PEEQ.append(np.max(data[::,23]))
    num -= 1
  return PEEQ, Rf2


def is_zero_frame(s):
    if s.split('.')[0].split('_')[-1]=='0':
        return True
    return False


def sort_files(files):
    frames = []
    for file in files:
        frames.append(int(file.split('.')[0].split('_')[-1]))
    df = pd.DataFrame(list(zip(frames, files)),
               columns =['Frame', 'File'])
    df = df.astype({'Frame':'int'})
    df.Frame = df.Frame.astype(float)
    df = df.sort_values('Frame')
    #print(df)
    #print(df.dtypes)
    return df['File'].tolist()


def sort_folds(folds):
    frames = []
    speed = {
    '001':'0.01',
    '01':'0.1',
    '1':'1',
    '10':'10'
    }
    for fold in folds:
        frames.append(float(fold.split('.')[0].split('_')[2]))
    df = pd.DataFrame(list(zip(frames, folds)),
               columns =['Frame', 'Folds'])
    df = df.astype({'Frame':'float'})
    #df.Frame = df.Frame.astype(float)
    df = df.sort_values('Frame')
    #print(df)
    #print(df.dtypes)
    return df['Folds'].tolist()    

path_to_main_folder = 'D:/VKR_PSCT/TXT_for_analysis/Геометрия'
folds = os.listdir(path_to_main_folder)
folders = sort_folds(folds)
path_figs = 'D:/VKR_PSCT/plots/Геометрия'
percantage = 0
size = len(folders)
count = 0
print('start')
plt.clf()
speed = {
    '001':'0.01',
    '01':'0.1',
    '1':'1',
    '10':'10'
    }
markers = [".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_",0,1,2,3,4,5,6,7,8,9,10,11]
for folder in folders:
    path = path_to_main_folder + '/' + folder
    f = os.listdir(path)
    files = sort_files(f)
    #print(files)
    
    zeroFrame = ''
    for file in files:
        if is_zero_frame(file):
            zeroFrame = file
            break
    
    #zeroFrame = 'Static_Rate_50_5_1_02_0.txt'
    #data = np.loadtxt(path + '/' + zeroFrame,dtype='double',skiprows=44)
    #print(data[::,0])

    #s = folder.split('.')[0].split('_')[4]
    num = len(files)
    #if speed[s] == '10':
    #    num = 9
    PEEQ, Rf2 = get_data_for_graph(path, files, num)
    # plt.figure()

    plt.xlabel("Деформация, -" )
    plt.ylabel("Усилие, МН")
    
    plt.plot(PEEQ, Rf2, label = folder.split('.')[0].split('_')[2]+', '+folder.split('.')[0].split('_')[3][:1]+'.'+folder.split('.')[0].split('_')[3][1:],marker = markers[count])

    
    count += 1
    
    
    percantage += 100 / size
    print('ready - %0.2f' % (percantage) + '%')
    
    
plt.legend(title = 'Ширина и высота, мм')
plt.savefig(path_figs + '/'+ 'graph_8.png', dpi=600)
plt.clf()
