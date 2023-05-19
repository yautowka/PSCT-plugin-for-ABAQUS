# -*- coding: utf-8 -*-
"""
Created on Sun May 14 11:20:17 2023

@author: LabPC_807
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def get_data_for_graph(path, files):
  Rf2 = []
  U2 = []
  speed = {
    '001':'0.01',
    '01':'0.1',
    '1':'1',
    '10':'10'
    }
  num = len(files)
  s = files[0].split('.')[0].split('_')[4]
  if speed[s] == '1':
      num -= 2 
  if speed[s] == '10':
      num = 7

  for file in files:
    if num==0:
        break
    anvil = np.loadtxt(path+'/'+file,dtype='double',skiprows=22,max_rows=1)
    Rf2.append(abs(anvil[8])/1000000)
    U2.append(abs(anvil[5])*1000)
    num -= 1

  return Rf2, U2


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
path_figs = 'D:/VKR_PSCT/plots/Геометрия/'
percantage = 0
size = len(folders)
print('start')
count = 2

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

    
    Rf2, U2 = get_data_for_graph(path, files)
    s = folder.split('.')[0].split('_')[4]
    plt.xlabel("Перемещение, мм" )
    plt.ylabel("Усилие, МН")
    plt.plot(U2, Rf2, label = folder.split('.')[0].split('_')[2]+', '+folder.split('.')[0].split('_')[3][:1]+'.'+folder.split('.')[0].split('_')[3][1:], marker = markers[count])
    
    count += 1

    #print('Скорость деформации = '+speed[s]+',Перемещение = '+str(max(U2))+',Усилие = '+str(max(Rf2)))
    
    
    percantage += 100 / size
    print('ready - %0.2f' % (percantage) + '%')
plt.legend(title = 'Ширина и высота, мм')
plt.savefig(path_figs + 'rf2_u2_from_anvil.png', dpi=600)
plt.clf()
