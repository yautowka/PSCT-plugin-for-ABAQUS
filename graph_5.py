# -*- coding: utf-8 -*-
"""
Created on Sat May 13 10:26:31 2023

@author: LabPC_807
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def get_ids_of_4_nodes(data):
  ids = []
  spots = []
  min1 = np.min(data[::,1])
  min2 = np.min(data[::,2])
  min3 = np.min(data[::,3])
  max2 = np.max(data[::,2])
  max3 = np.max(data[::,3])
  for i in range(len(data[::,0])):
    coord1 = data[i,1]
    coord2 = data[i,2]
    coord3 = data[i,3]
    if coord1 == min1:
      if coord2 == min2:
        if coord3 == min3:
          ids.append(i)
          spots.append('left bottom')
        if coord3 == max3:
          ids.append(i)
          spots.append('right bottom')
      if coord2 == max2:
        if coord3 == min3:
          ids.append(i)
          spots.append('left top')
        if coord3 == max3:
          ids.append(i)
          spots.append('right top')
  return ids, spots


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

def get_ids_of_4graph(data):
    map_Of_ids = dict()
    min1 = np.min(data[::,1])
    max3 = np.max(data[::,3])
    min3 = np.min(data[::,3])
    for i in range(len(data[::,0])):
        coord2 = data[i,2]
        coord3 = data[i,3]
        if coord3 == min3:
            map_Of_ids.setdefault(coord2,[]).append(i) 
    return map_Of_ids, min1, max3

def get_breadth_and_distance(ids_for_4graph, path, file, min1, max3):
    half_breadth = []
    distance = []
    data = np.loadtxt(path + '/' + file,dtype='double',skiprows=44)
    #print(ids_for_3graph)
    for i in ids_for_4graph:
        half_breadth.append(abs(data[i,3] - max3))
        distance.append(abs(data[i,1] - min1))
    return half_breadth, distance

def get_max_strain(ids, path, file):
    data = np.loadtxt(path + '/' + file,dtype='double',skiprows=44)
    max_value = 0
    for i in ids:
       max_value = max(abs(data[i, 23]), max_value)
    return max_value

def get_lists(min_temp1,min_temp2,max_temp1,max_temp2):
    labelsX = []
    ticksX = []
    labelsY = []
    ticksY = []
    
    min_x = min_temp1
    min_y = min_temp2
    max_x = max_temp1
    max_y = max_temp2
    
        
    while min_x <= max_x:
        labelsX.append(str(int(min_x*1000)))
        ticksX.append(min_x)
        min_x += 0.005
    while min_y <= max_y:
        labelsY.append(str(int(min_y*10000)/10))
        ticksY.append(min_y)
        min_y += 0.0005
    
    
    return labelsX, ticksX, labelsY, ticksY

def get_diff(path):
    anvil = np.loadtxt(path,dtype='double',skiprows=22,max_rows = 1)
    data = np.loadtxt(path,dtype='double',skiprows=44)
    diff = abs(np.max(data[::,2]) - anvil[2])
    h0 = abs(np.max(data[::,2]) - np.min(data[::,2]))
    b0 = abs(np.max(data[::,3]) - np.min(data[::,3]))
    return diff, h0, b0
    

def get_data_for_graph(diff, h0, b0, path, files):
    h_h0 = []
    b_b0 = []
    count = 0
    for file in files[::int(len(files)/10)+1]:
       #if file.split('.')[0].split('_')[4]=='10' and count>4:
       #    break
       anvil = np.loadtxt(path + '/' + file,dtype='double',skiprows=22,max_rows = 1)
       data = np.loadtxt(path + '/' + file,dtype='double',skiprows=44)
       h_h0.append(abs(abs(anvil[2] - diff) - abs(np.min(data[::,2])))/h0)
       b_b0.append(abs(np.max(data[::,3]) - np.min(data[::,3]))/b0)
       count += 1
    return h_h0, b_b0


def sort_folds(folds):
    frames = []
    for fold in folds:
        frames.append(int(fold.split('.')[0].split('_')[2]))
    df = pd.DataFrame(list(zip(frames, folds)),
               columns =['Frame', 'Folds'])
    df = df.astype({'Frame':'int'})
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
print('start')
count = 0
speed = {
    '001':'0.01',
    '01':'0.1',
    '1':'1',
    '10':'10'
    }
plt.clf()


markers = [".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_",0,1,2,3,4,5,6,7,8,9,10,11]
for folder in folders:
    
        
    
    path = path_to_main_folder + '/' + folder
    f = os.listdir(path)
    files = sort_files(f)
    #print(files)
    print(folder)
    zeroFrame = ''
    for file in files:
        if is_zero_frame(file):
            zeroFrame = file
            break
    

    #data = np.loadtxt(path + '/' + zeroFrame,dtype='double',skiprows=44)

    diff, h0, b0 = get_diff(path + '/' + zeroFrame)    #разница между нижней точкой anvil и его координатой

    h_h0, b_b0 = get_data_for_graph(diff, h0, b0, path, files)

    plt.plot(h_h0, b_b0, label = folder.split('.')[0].split('_')[2]+', '+folder.split('.')[0].split('_')[3][:1]+'.'+folder.split('.')[0].split('_')[3][1:], marker = markers[count])

    #plt.title(folder)
    
    #labelsX, ticksX, labelsY, ticksY = get_lists(min_temp1,min_temp2,max_temp1,max_temp2)
    plt.xlabel("h/h0, -" )
    plt.ylabel("b/b0, -")
    #plt.xticks(ticksX, labelsX)
    #plt.yticks(ticksY, labelsY)
    
    #plt.savefig(path_figs +'/'+ folder + '_graph5.png', dpi=600)
    #plt.clf()
    percantage += 100 / size
    print('ready - %0.2f' % (percantage) + '%')
    count += 1
plt.legend(title = 'Ширина и высота, мм')
#+' с'+"\u207B\u00B9"
plt.savefig(path_figs +'/'+ 'graph5.png', dpi=600)
plt.clf()