import time
import os
import json
import requests
import cv2
import datetime
import pandas as pd

from bs4 import BeautifulSoup
from fake_headers import Headers

from managers.FileManager import FileManager as fm
from managers.ProxyManager import ProxyManager as pm
from util.Logger import Logger as l


class DataManager:
    '''
    Класс отвечает за получение и загрузку данных
    '''

    def __init__(self, config):
        self.proxy = pm()
        self.config = config
        self.fake_header = Headers(browser="chrome", os="win", headers=True)

    def download_images(self, name, need_count):
        '''
        Ищем изображения по запросу
        @name - запрос
        @need_count - необходимое количество изображений
        '''
        urls_used = fm.get_used_url(name)
        page = fm.get_last_page(name)
        query = str.replace(name, ' ', '%20')
        path = fm.get_sources_path(name)
        jpg_files = os.listdir(path)
        current_count = len(jpg_files)
        file_number = current_count

        # ищем ссылки на оригинальные изображения
        while current_count < need_count:
            urls_new = self.__parse_page(page, query)
            urls = list(set(urls_new) - set(urls_used))
            l.print_i(f'Найдено {len(urls)} urls')

            with open(fm.get_used_url_path(name), 'a', encoding="utf-8") as file:
                for url in urls:
                    file_name = str(file_number) + '.jpg'
                    load = self.__download(name, url, file_name, 0)
                    urls_used.append(url)
                    file.write(url+"\n")
                    if load:
                        file_number += 1
                        current_count += 1
            l.print_sub_g(f'Загружено {current_count} изображений из {need_count}')
            page += 1
            fm.save_last_page(name, page)
        l.print_g(f'Все изображения {name} загружены')

    def __print_info(self, url, proxy, headers):
        '''
        Выводим информацию о текущем подключении
        @url - ссылка по которой подключаемся
        @proxy - ip proxy
        @headers - заголовки строки подключения
        '''

        print()
        print(f'URL: {url}')
        print(f'Proxy: {proxy}')
        print(f'Headers UA: {headers}')

    def __get_html(self, page, query, use_last=False):
        '''
        Получение кода html страницы
        @page - номер страницы
        @query - запрос
        '''
        url = f'https://yandex.ru/images/touch/search?from=tabbar&p={page}&text={query}&itype=jpg'
        header = self.__get_headers()
        proxies = self.proxy.get() if use_last else self.proxy.get_next()
        if proxies['http'] == '':
            l.print_i('Новая итерация по списку прокси')
            self.__await(30)

        self.__print_info(url, proxies, header)

        try:
            response = requests.get(url, headers=header, timeout=(
                3, 10), proxies=proxies, verify=False)
        except Exception as e:
            l.print_e(f'{e.__class__.__name__}: {url}')
            self.__await(1)
            return self.__get_html(page, query)
        l.print_sub_g('Подключились')
        return response.content

    def __parse_page(self, page, query):
        '''
        Разбор кода html страницы
        @page - номер страницы
        @query - запрос
        '''

        # получаем содержимое страницы
        div = None
        use_last = True
        while div is None:
            content = self.__get_html(page, query, use_last)
            root = BeautifulSoup(content, 'html.parser')
            div = root.find('div', class_="Root",
                            id=lambda x: x and x.startswith('ImagesApp-'))
            # проверка на капчу
            if div is None:
                print(f'Капча на {page} странице.')
                use_last = False
                self.__await(1)

        data_state = div.get('data-state')
        jdata = json.loads(data_state)
        jent = jdata['initialState']['serpList']['items']['entities']

        links = []
        # получаем url изображений
        for item in jent:
            # image - аватары изображений, originUrl - изображения в оригинальном формате
            if self.config.image_small:
                url = 'http:' + jent[item]['image']
                print(url)
                links.append(url)
            else:
                url = jent[item]['originUrl']
                print(url)
                links.append(url)

        return links

    def __get_headers(self):
        '''
        Получение случайного заголовка страницы
        '''
        header = self.config.header
        if self.config.generate_header:
            header = self.fake_header.generate()

        return header

    def __download(self, query, url, file_name, count_load):
        '''
        Скачивание изображения по ссылке
        @query - запрос
        @url - ссылка на изображение
        @nameFile - название файла
        @count_load - количество попыток загрузки
        '''
        header = self.__get_headers()
        path = fm.get_sources_path(query)
        path_image = path + '\\' + file_name
        try:
            with requests.get(url, headers=header, stream=True, timeout=(5, 15), verify=False) as r:
                with open(path_image, 'wb') as f:
                    f.write(r.content)
                    print(f'Скачан файл [{file_name}]: {url}')
        except requests.exceptions.SSLError as e:
            # Узнаем имя возникшего исключения
            l.print_e(f'{e.__class__.__name__}: {url}')
            return False
        except requests.exceptions.ConnectionError as e:
            # Узнаем имя возникшего исключения
            l.print_e(f'{e.__class__.__name__}: {url}')
            self.__await(5)
            if count_load > 5:
                return False
            return self.__download(query, url, file_name, count_load + 1)
        except Exception as e:
            # Узнаем имя возникшего исключения
            l.print_e(f'{e.__class__.__name__}: {url}')
            self.__await(3)
            if count_load <= 1:
                return self.__download(query, url, file_name, count_load + 1)
            return False

        valid_image = self.check_image(path_image, query)
        if valid_image:
            path_annot = fm.get_annotation_path(query)
            if not os.path.exists(path_annot):
                cols = ['date', 'url', 'file_name']
                df = pd.DataFrame(data=cols)
                df.to_csv(path_annot, index=False, mode='a')

            today = datetime.datetime.today()
            data_list = []
            data_list.append((today.strftime("%d-%m-%Y-%H.%M.%S"), url, file_name))
            df = pd.DataFrame(data=data_list)
            df.to_csv(path_annot, header=False, index=False, mode='a')
        return valid_image

    def __await(self, sec):
        '''
        Ожидание с выводом в консоль
        @sec - количество секунд
        '''
        for i in range(sec, 0, -1):
            print(f'Ждем: {i:03} s', end='\r')
            time.sleep(1)

    def indexation(self, name):
        '''
        Изменение номеров файлов по порядку 0000, 0001 ...
        @name - запрос
        '''
        path = fm.get_sources_path(name)
        path_annot = fm.get_annotation_path(name)
        
        df = pd.read_csv(path_annot)
        headers = df[0]
        df.drop(0, inplace=True)
        images_count = len(df)
        digit_len = len(str(images_count))
        
        # Создаём список файлов в папке
        initial_number = 0
        # Перебираем каждый файл и увеличиваем порядковый номер
        for row in df:
            file_name = row['file_name']
            os.rename(f'{path}\\{file_name}', f'{path}\\temp_{initial_number}.jpg')
            row['file_name'] = file_name
            initial_number += 1

        initial_number = 0
        for row in df:
            file_name = row['file_name']
            index = str(initial_number).zfill(digit_len)
            os.rename(f'{path}\\{file_name}', f'{path}\\{index}.jpg')
            initial_number += 1
        df.append()
        ndf = pd.DataFrame(data = df, headers = headers)
        ndf.to_csv(path_annot, index=False)

    def open_or_delete(self, path):
        '''
        Проверяет возможность открытия файла как изображения, в случае невозможности открытия удаляет файл
        @path - путь к файлу
        @return - если файл не валиден, иначе изображение
        '''
        image = cv2.imread(path)
        if image is None:
            os.remove(path)
            l.print_w('Удалено невалидное изображение')
        return image

    def resize_image(self, image, path):
        '''
        Изменение размера изображения
        @image - загруженное изображение
        @query - текст запроса
        '''
        size = self.config.image_size
        image = cv2.resize(image, size)
        cv2.imwrite(path, image)
        return image

    def delete_if_exist(self, image, query, path_image):
        '''
        Проверяет есть ли дубликаты изображения, если есть, удаляет файл
        @image - загруженное изображение
        @query - текст запроса
        @path_image - ссылка на изображения
        @return - None, если файл не валиден, иначе изображение
        '''
        path = fm.get_sources_path(query)
        file_names = os.listdir(path)
        for name in file_names:
            path_file = f'{path}\\{name}'
            if path_image == path_file:
                continue

            image_file = cv2.imread(path_file)
            if (image == image_file).all():
                os.remove(path_image)
                l.print_w('Такое изображение уже загружено! Копия удалена')
                return False
        return True

    def check_image(self, path, query):
        '''
        Проверяет нужно ли это изображение, приводит к общему формату
        @param path - путь до изображения
        @param query - текст запроса
        @return True - изображение подходит, иначе False
        '''
        image = self.open_or_delete(path)
        if image is None:
            return False
        image = self.resize_image(image, path)
        return self.delete_if_exist(image, query, path)

    def create_dataset_from_files(self, queries):
        cols = ['absolute_path', 'relate_path', 'tag']
        data_matrix = []
        for query in queries:
            path = fm.get_sources_path(query)
            for file in os.listdir(path):
                relative = f'{path}\\{file}'
                absolute = os.path.abspath(relative)
                data_matrix.append((absolute, relative, query))

        return pd.DataFrame(data=data_matrix, columns=cols)

    def save_new_dataset(self, queries, index_custom=False):
        file_name = ''
        for query in queries:
            file_name +=f'[{query}]'
        path = fm.create_annotation_folder() +f'\\{file_name}.csv'
        dataset = self.create_dataset_from_files(queries)
        dataset.to_csv(path, index=index_custom)
        l.print_g(f'Cоздан dataset: {file_name}.csv')