import os
import os.path
from time import sleep
from shutil import copy
from collections import defaultdict
from util.iterators import Iterator
import pandas as pd

def create_folder(path):
    '''
    Cоздает папки по адресу
    @path - путь к папке
    @return - путь к папке
    '''
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def awaits(sec):
    '''
    Ожидание с выводом в консоль
    @sec - количество секунд
    '''
    for i in range(sec, 0, -1):
        print(f'Ждем: {i:03} s', end='\r')
    sleep(1)

def get_row(path, tag):
    relative_path = path
    absolute_path = os.path.abspath(relative_path)
    return [absolute_path, relative_path, tag]

def get_images(path):
    df = pd.read_csv(path, usecols=['relate_path', 'tag'])
    return df.iterrows()
    
def copy_dataset_to_rand(to_folder, ann_path, ann_directory): 
    '''
    Копирует файлы содержащиеся в аннотациях исходных папок 
    в формате 0.jpg
    @to_folder - адрес куда нужно скопировать изображения
    @ann_path - адрес исходного файла-аннотации
    @ann_directory - адрес директории с аннотациями
    @return - название файла аннотации
    '''
    data_matrix = []
    for index, row in get_images(ann_path):
        path_from = row['relate_path']
        tag = row['tag']
        path_to = to_folder + f'\\{index}.jpg'
        copy(path_from, path_to)
        row = get_row(path_to, tag)
        data_matrix.append(row)

    cols = ['absolute_path', 'relate_path', 'tag']
    df = pd.DataFrame(data=data_matrix, columns=cols)
    df.to_csv(f'{to_folder}\\info.csv', index=False)
    folder_name = os.path.basename(ann_path)
    full_name = f'rand_{folder_name}'
    copy(f'{to_folder}\\info.csv', f'{ann_directory}\\{full_name}')
    return full_name

def copy_dataset_to_tag(to_folder, ann_path, ann_directory):
    '''
    Копирует файлы содержащиеся в аннотациях исходных папок 
    в формате classname_0000.jpg
    @to_folder - адрес куда нужно скопировать изображения
    @ann_path - адрес исходного файла-аннотации
    @ann_directory - адрес директории с аннотациями
    @return - название файла аннотации
    '''
    data_matrix = []
    for _, row in get_images(ann_path):
        path_from = row['relate_path']
        tag = row['tag']
        file_name = os.path.basename(path_from)
        path_to = to_folder + f'\\{tag}_{file_name}'
        copy(path_from, path_to)
        row = get_row(path_to, tag)
        data_matrix.append(row)

    cols = ['absolute_path', 'relate_path', 'tag']
    df = pd.DataFrame(data=data_matrix, columns=cols)
    df.to_csv(f'{to_folder}\\info.csv', index=False)
    folder_name = os.path.basename(ann_path)
    full_name = f'tag_{folder_name}'
    copy(f'{to_folder}\\info.csv', f'{ann_directory}\\{full_name}')
    return full_name

def get_iters_from_annotations(path_annot):
    iters = defaultdict(list)
    df = pd.read_csv(path_annot)
    for _, row in df.iterrows():
        iters[row['tag']].append(row['absolute_path'])
        
    res = {}
    for key, value in iters.items():
        res[key] = Iterator(value)
    return res



