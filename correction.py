# -*- coding: utf-8 -*-
"""
Created on Sun May 14 12:19:07 2023

@author: LabPC_807
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import math

def get_Cb(path, fileLast, b0, h0):
    diff = 0.0001 #расстояние от инструмента до заготовки по 2 оси
    anvil = np.loadtxt(path+'/'+fileLast,dtype='double',skiprows=22,max_rows=1)
    data = np.loadtxt(path+'/'+fileLast,dtype='double',skiprows=44)
    min2 = np.min(data[::,2]) #нижняя координата заготовки
    h_last = abs(anvil[2]-diff-min2)*2 #высота на последнем фрейме
    b_last = abs(np.max(data[::,3]) - np.min(data[::,3]))*2 #ширина на последнем фрейме
    w = 15/1000 #ширина инструмента
    coord_w = anvil[1] - w/4 # координата стенки инструмента
    diff_for_b = 0.001 #из-за дискретности нужно взять разброс
    temp_b_last = 10 #координата узла, который расширится вдоль стенки иструмента
    for i in range(len(data[::,0])):
        if abs(data[i,1] - coord_w) < diff_for_b:
            temp_b_last = min(temp_b_last, data[i,3])
        
    b5 = abs(temp_b_last - np.max(data[::,3]))*2
    
    bf = (2 * b0 + (b5 * 2 + b_last)/3)/3 #т.к. в статье проводились измерения равных величин(в случае реального эксперемента), а в нашем случае мы можем точно узнать ширину и высоту
    hf = (4 * h0 + h_last)/5
    
    Cb = ((bf/b0) - 1)/(1 - pow(hf/h0, 0.5))
    return Cb
 
def get_data_for_graph(path, files, c, b0, h0, friction):
  b = []
  data = np.loadtxt(path+'/'+files[0],dtype='double',skiprows=44)
  min2 = np.min(data[::,2]) #нижняя координата заготовки, чтобы находить высоту
  z0 = []
  hs = []
  for file in files:
    anvil = np.loadtxt(path+'/'+file,dtype='double',skiprows=22,max_rows=1)
    h = abs(anvil[2] - 0.0001 - min2)*2 #0.0001 разница координаты интсруменат и верха заготовки
    hs.append(h)
    b.append(b0 * (1 + c - c * pow(h/h0,0.5) ))
    z0.append( (h/(2*friction)) * math.log(1/(2*friction)) )
  return b, z0, hs

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
        frames.append(float(speed[fold.split('.')[0].split('_')[4]]))
    df = pd.DataFrame(list(zip(frames, folds)),
               columns =['Frame', 'Folds'])
    df = df.astype({'Frame':'float'})
    #df.Frame = df.Frame.astype(float)
    df = df.sort_values('Frame')
    #print(df)
    #print(df.dtypes)
    return df['Folds'].tolist() 

def get_pressure(path, files, b, w):
    pressure  = []
    strain = []
    num = 0
    for file in files:
        anvil = np.loadtxt(path+'/'+file,dtype='double',skiprows=22,max_rows=1)
        force = anvil[8]
        pressure.append(abs(force/(b[num]*w))/1000000)
        num += 1
        data = np.loadtxt(path+'/'+file,dtype='double',skiprows=44)
        strain.append(np.max(data[::,23]))
    return pressure, strain

def get_2k(z0, b, w, h, pressure, friction):
    two_k = []
    #формулы из статьи
    for i in range(len(z0)):
        if z0[i]*2 > w:
            p = pressure[i]
            first = 1/(b[i]*w)
            second = 2*(h[i]**2)/(friction**2) + (b[i]-w)*h[i]/friction
            third = math.exp(friction*w/h[i]) - 1
            fourth = 2*h[i]/(friction*b[i])

            result = p/(first*second*third-fourth)
            two_k.append(result)
        if z0[i] >= 0 and z0[i]*2 < w:
            p = pressure[i]
            first = h[i]/(friction*w)
            second = 1/(2*friction) - 1 
            third = (w/2 - z0[i])/(friction*w)
            fourth = ((w/2 - z0[i])**2)/(h[i]*w)
            fifth = 1/(friction*b[i])
            sixth = 2*(z0[i]**2)/w - z0[i] - 2*h[i]*z0[i]/(friction*w) + h[i]/(2*friction) - h[i] + (h[i]**2)/(w*(friction**2)) - 2*(h[i]**2)/(friction*w)
            seventh = 1/(h[i]*b[i])
            eighth = z0[i]**2 - 4*(z0[i]**3)/(3*friction) - (w**2)/12
            result = p/(first*second+third+fourth+fifth*sixth+seventh*eighth)
            two_k.append(result)
        if z0[i] < 0:
            p = pressure[i]
            first = 1
            second = w/(4*h[i])
            third = (w**2)/(12*h[i]*b[i])
            result = p/(first+second-third)
            two_k.append(result)
            
    return two_k
    
def get_f(b,h):
    fe3 = math.log(h[-1]/h[0])
    fe2 = math.log(b[-1]/b[0])
    fe = 2*((fe2**2+fe2*fe3+fe3**2)**0.5)/(math.sqrt(3))
    f = -fe/fe3 #поиск коэффициента f и получение по формуле из статьи эквивалентной деформации
    eq_strain = []
    for i in range(len(b)):
        e3 = math.log(h[i]/h[0])
        e2 = math.log(b[i]/b[0])
        e = 2*((e2**2+e2*e3+e3**2)**0.5)/(math.sqrt(3))
        eq_strain.append(e)
    #print('e2:'+str(e2))
    #print('e3:'+str(e3))
    #print('e:'+str(e))
    #print('f:'+str(f))
    return f, eq_strain
 
def do_correction2(path, files, h0, v0):
    strain = []
    stress = []
    for file in files:
        anvil = np.loadtxt(path+'/'+file,dtype='double',skiprows=22,max_rows=1)
        force = abs(anvil[8]/1000000)
        U2 = abs(anvil[5])
        
        strain.append( (2/math.sqrt(3)) * math.log(h0/ (h0-U2)) )
        stress.append( (math.sqrt(3)/2) * force * (h0-U2) / v0)
    return strain, stress


path_to_main_folder = 'D:/VKR_PSCT/TXT_for_analysis/Трение_2'
folds = os.listdir(path_to_main_folder)
folders = sort_folds(folds)
path_figs = 'D:/VKR_PSCT/plots/Трение_2/'
percantage = 0
size = len(folders)
print('start')
markers = [".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_",0,1,2,3,4,5,6,7,8,9,10,11]
for folder in folders:
    if folder.split('.')[0].split('_')[5]=='00': # пропускаем трение 0
        continue
    print(folder)
    path = path_to_main_folder + '/' + folder
    f = os.listdir(path)
    files = sort_files(f) # сортировка фреймов
    #print(files)
    
    
    b0 = float(folder.split('.')[0].split('_')[2])/1000
    h0 = float(folder.split('.')[0].split('_')[3])/1000 # имя папки хранит начальные параметры
    friction = float(folder.split('.')[0].split('_')[5])/10
    l0 = 70/1000
    v0 = b0*h0*l0
    strain_from_correction2, stress_from_correction2 = do_correction2(path, files, h0, v0)
    print('Трение = ' + str(friction))
    C = get_Cb(path, files[-1], b0, h0)
    b, z0, h = get_data_for_graph(path, files, C, b0, h0, friction)
    w = 15/1000 #ширина инструмента
    pressure, strain = get_pressure(path, files, b, w)
    
    
    
    #print(friction)
    two_k = get_2k(z0, b, w, h, pressure, friction)
    #print(two_k)
    plt.xlabel("Эквивалентная деформация, -" )
    plt.ylabel("Напряжение, Мпа")
    f, eq_strain = get_f(b,h)
    
    amount = len(eq_strain)
    for i in range(len(eq_strain)):
       if eq_strain[i]>=1:
            amount = i
            break
    
    plt.plot(eq_strain[:amount], pressure[:amount], label = 'Напряжение без корректировки')
    #plt.plot(strain, two_k, label = '2k')
    
    #print('f = '+str(f))
    result = [i / f for i in two_k]
    plt.plot(eq_strain[:amount], result[:amount], label = 'Напряжение с корректировкой')
    #plt.plot(strain_from_correction2,stress_from_correction2, label = 'Напряжение с корректировкой по вторым формулам')
    plt.legend()
    #plt.show()
    plt.savefig(path_figs + folder + '_correction.png', dpi=600)
    plt.clf()
    
    
    
    
    percantage += 100 / size
    print('ready - %0.2f' % (percantage) + '%')
