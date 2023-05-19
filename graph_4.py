# -*- coding: utf-8 -*-
"""
Created on Sat May  6 18:30:14 2023

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


def get_data_for_graph(path, files, ids):
  PEEQ1 = []
  Mises1 = []
  PEEQ2 = []
  Mises2 = []
  PEEQ3 = []
  Mises3 = []
  PEEQ4 = []
  Mises4 = []
  Times = []
  Rf2 = []
  U21 = []
  U22 = []
  U23 = []
  U24 = []
  for file in files:
    
    time = np.loadtxt(path+'/'+file,dtype='str',skiprows=8,max_rows=1)[-1]
    Times.append(time)
    rf = np.loadtxt(path+'/'+file,dtype='double',skiprows=22,max_rows=1)[8]
    Rf2.append(abs(rf))
    #print(time)
    
    data1 = np.loadtxt(path+'/'+file,dtype='double',skiprows=44+ids[0],max_rows=1)
    data2 = np.loadtxt(path+'/'+file,dtype='double',skiprows=44+ids[1],max_rows=1)
    data3 = np.loadtxt(path+'/'+file,dtype='double',skiprows=44+ids[2],max_rows=1)
    data4 = np.loadtxt(path+'/'+file,dtype='double',skiprows=44+ids[3],max_rows=1)
    PEEQ1.append(data1[23])
    PEEQ2.append(data2[23])
    PEEQ3.append(data3[23])
    PEEQ4.append(data4[23])
    
    Mises1.append(data1[10])
    Mises2.append(data2[10])
    Mises3.append(data3[10])
    Mises4.append(data4[10])
    
    U21.append(abs(data1[5]))
    U22.append(abs(data2[5]))
    U23.append(abs(data3[5]))
    U24.append(abs(data4[5]))


  return PEEQ1, Mises1, PEEQ2, Mises2, PEEQ3, Mises3, PEEQ4, Mises4, Times, Rf2, U21, U22, U23, U24


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
        half_breadth.append(abs(data[i,3] - max3)*1000)
        distance.append(abs(data[i,1] - min1)*1000)
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

path_to_main_folder = 'D:/VKR_PSCT/TXT_for_analysis/Геометрия'
folders = os.listdir(path_to_main_folder)
path_figs = 'D:/VKR_PSCT/plots/Геометрия/'
percantage = 0
size = len(folders)
print('start')
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
    

    data = np.loadtxt(path + '/' + zeroFrame,dtype='double',skiprows=44)


    map_of_ids_for_4graph, min1, max3 = get_ids_of_4graph(data)
    file = files[-1]
    if folder.split('.')[0].split('_')[4]=='10':
        file = files[8]
    num = 0
    for key in map_of_ids_for_4graph.keys():
        #print(map_of_ids_for_4graph.get(key))
        half_breadth, distance = get_breadth_and_distance(map_of_ids_for_4graph.get(key), path + '/', file, min1, max3)
        max_strain = get_max_strain(map_of_ids_for_4graph.get(key), path + '/', file)
        plt.plot(distance, half_breadth, label = str(max_strain), marker = markers[num])
        num += 1
    plt.title(folder)
    
    plt.xlabel("Расстояние от центральной линии, мм" )
    plt.ylabel("Половина ширины, мм")
    plt.legend(title = 'Деформация, -')
    plt.savefig(path_figs +'/'+ folder + '_graph4.png', dpi=600)
    plt.clf()
    percantage += 100 / size
    print('ready - %0.2f' % (percantage) + '%')



