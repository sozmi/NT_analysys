from managers.FileManager import FileManager as fm
from shutil import copy
from util.Iterators import Iterator
import pandas as pd
from collections import defaultdict

class Script():

    def copy_to_dataset_up(queries): 
        '''
        Копируем из dataset/class/0000.jpg должно получиться dataset/class_0000.jpg
        @queries - запросы
        '''
        cols = ['absolute_path', 'relate_path', 'tag']
        data_matrix = []
        for query in queries:
            path_annot = fm.get_annotation_path(query)
            path_from = fm.get_sources_path(query)
            path_to = fm.get_ds_folder()

            file_names = pd.read_csv(path_annot, header=None, columns = [2])
            # Перебираем каждый файл и увеличиваем порядковый номер
            for name in file_names:
                absolute = f'{path_from}//{name}'
                relative = f'{path_to}//{query}_{name}'
                copy(absolute, relative)
                data_matrix.append((absolute, relative, query))

        df = pd.DataFrame(data=data_matrix, columns=cols)
        df.to_csv(f'{path_to}\\annotation.csv', index = False)


    def copy_to_dataset_up(queries): 
        '''
        Копируем из dataset/class/0000.jpg должно получиться dataset/class_0000.jpg
        @queries - запросы
        '''
        cols = ['absolute_path', 'relate_path', 'tag']
        data_matrix = []
        for query in queries:
            path_annot = fm.get_annotation_path(query)
            path_from = fm.get_sources_path(query)
            path_to = fm.get_ds_folder()

            file_names = pd.read_csv(path_annot, header=None, columns = [2])
            # Перебираем каждый файл и увеличиваем порядковый номер
            for name in file_names:
                absolute = f'{path_from}//{name}'
                relative = f'{path_to}//{query}_{name}'
                copy(absolute, relative)
                data_matrix.append((absolute, relative, query))

        df = pd.DataFrame(data=data_matrix, columns=cols)
        df.to_csv(f'{path_to}\\annotation_class.csv', index = False)
    
    def copy_dataset_number(queries):
        '''
        Копируем из dataset/class/0000.jpg должно получиться dataset/class_0000.jpg
        @queries - запросы
        '''
        cols = ['absolute_path', 'relate_path', 'tag']
        data_matrix = []
        i = 0
        for query in queries:
            path_annot = fm.get_annotation_path(query)
            path_from = fm.get_sources_path(query)
            path_to = fm.get_ds_folder()

            file_names = pd.read_csv(path_annot, header=None, columns = [2])
            # Перебираем каждый файл и увеличиваем порядковый номер
            for name in file_names:
                absolute = f'{path_from}//{name}'
                relative = f'{path_to}//{str(i)}.jpg'
                i += 1
                copy(absolute, relative)
                data_matrix.append((absolute, relative, query))

        df = pd.DataFrame(data=data_matrix, columns=cols)
        df.to_csv(f'{path_to}\\annotation_number.csv', index = False)

    def get_iters_from_annotations(path_annot):
        iters = defaultdict(list)
        df = pd.read_csv(path_annot)
        for index, row in df.iterrows():
            iters[row['tag']].append(row['absolute_path'])
        
        res = {}
        for key, value in iters.items():
            res[key] = Iterator(value);
        return res





