from email.mime import image
from random import randint
from tkinter import Image
from turtle import down
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
from managers.FileManager import FileManager as fm

import shutil
import requests
import os
import time
import json
import cv2

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DataManager(object):
    '''
    Класс отвечает за получение и загрузку данных
    '''
    frp = FreeProxy(rand=True)
    lastProxies = {}
    blackProxy =[]
    

    def downloadImages(name, need_сount):
        '''
        Ищем изображения по запросу
        @name - запрос
        @need_count - необходимое количество изображений
        @need_small - нужно ли загружать миниатюры
        '''
        usedURL = fm.getUsedUrl(name)
        page = fm.getLastPage(name)
        query = str.replace(name,' ','%20')
        path = fm.getSourcesPath(name)
        jpg_files = os.listdir(path)
        imagesCount = len(jpg_files)
        number_file = imagesCount

        #ищем ссылки на оригинальные изображения
        while imagesCount < need_сount: 
            urls = DataManager.__parsePage(page, query)
            actualUrl = list(set(urls) - set(usedURL))
            print(f'Найдено {len(actualUrl)} urls')
            
            with open(fm.getUsedUrlPath(name), 'a') as file:
                for url in actualUrl:
                    nameFile = str(number_file) + '.jpg'
                    isLoaded = DataManager.__download(name, url, nameFile, 0)
                    usedURL.append(url)
                    file.write(url+"\n")
                    if isLoaded == True:
                        number_file+=1
                        imagesCount+=1
            print(f'{bcolors.OKCYAN} Загружено {imagesCount} изображений из {need_сount} {bcolors.ENDC} ')
            page+=1
            fm.saveLastPage(name,page)

    def __printInfoConnect(url, proxy, headers):
        '''
        Выводим информацию о текущем подключении
        @url - ссылка по которой подключаемся
        @proxy - ip proxy
        @headers - заголовки строки подключения
        '''
        if not proxy:
            proxy = 'no'

        print()
        print(f'URL: {url}')
        print(f'Proxy: {proxy}')
        print(f'Headers UA: {headers}')


    def __getHtml(page, query, needProxy):
        '''
        Получение кода html страницы
        @page - номер страницы
        @query - запрос
        @needProxy - нужно ли использовать прокси при подключении
        '''
        URL = f'https://yandex.ru/images/touch/search?from=tabbar&p={page}&text={query}&itype=jpg'
        HEADERS = DataManager.__getHeaders()
        proxies = DataManager.lastProxies
        proxy = ''
        if(needProxy):
            print('Ищем работающий прокси...')
            while not proxies:
                try:
                    proxy = DataManager.frp.get()
                    if(proxy in DataManager.blackProxy):
                        print(f'Прокси {proxy} в черном списке')
                        continue
                    proxies = { 'http': proxy, 'https': proxy }
                    DataManager.lastProxies = proxies
                except Exception as e:
                    # Узнаем имя возникшего исключения
                    print(e.__class__.__name__ + ' in find proxy')  
                    DataManager.__await(5);
                    DataManager.lastProxies = ''
                    print(f'{bcolors.OKBLUE}Очищен черный список прокси{bcolors.ENDC}')
                    DataManager.blackProxy.clear();
    
        
        DataManager.__printInfoConnect(URL, proxies, HEADERS)

        try:
            response = requests.get(URL, headers=HEADERS, timeout=(3.05, 5), proxies=proxies, verify=False)
        except Exception as e:
            # Узнаем имя возникшего исключения
            print(e.__class__.__name__ + f': {URL}') 
            DataManager.lastProxies = ''
            DataManager.blackProxy.append(proxy)
            return DataManager.__getHtml(page, query, True)

        print('Connected')
        
        return response.content


    def __parsePage(page,query):
        '''
        Разбор кода html страницы
        @page - номер страницы
        @query - запрос
        '''
        content = DataManager.__getHtml(page, query, False)
        #получаем содержимое страницы
        rootDiv = None
        while rootDiv is None:
            root = BeautifulSoup(content, 'html.parser')
            rootDiv = root.find('div', class_="Root", id=lambda x: x and x.startswith('ImagesApp-'))
            #проверка на капчу
            if(rootDiv is None):
                DataManager.lastProxies = {}
                print(f'Капча на {page} странице.') 
                content = DataManager.__getHtml(page, query, True)

        dataState = rootDiv.get('data-state');
        jdata = json.loads(dataState)
        jent = jdata['initialState']['serpList']['items']['entities']
        
        links = []
        #получаем url оригинальных изображений
        for item in jent:
            url = jent[item]['origUrl'];
            print(url)
            links.append(url)

        return links


    def __getHeaders():
         '''
         Получение случайного заголовка страницы
         '''
         ua = UserAgent(os='windows',min_percentage=40)
         headers = {'User-Agent': ua.random,
                   'Accept-Encoding': 'gzip, deflate, br, zstd',
                   'Accept-Language': 'ru,en;q=0.9',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
                   }
         return headers

    def __download(name, url, nameFile, numLoad):
        '''
        Скачивание изображения по ссылке
        @name - запрос
        @url - ссылка на изображение
        @nameFile - название файла
        @newLoad - индикатор первый ли вызов функции
        '''
        HEADERS = DataManager.__getHeaders()
        path = fm.getSourcesPath(name);
        imagePath = path +'\\'+nameFile;
        try:
            with requests.get(url, headers = HEADERS, stream=True, timeout=(5,15)) as r:
                with open(imagePath, 'wb') as f:
                    f.write(r.content)
                    #shutil.copyfileobj(r.raw, f)
                    print(f'Скачан файл [{nameFile}]: {url}') 
        except requests.exceptions.SSLError as e:
            # Узнаем имя возникшего исключения
            print(f'{bcolors.FAIL}{e.__class__.__name__}: {url}{bcolors.ENDC}')
            return False
        except requests.exceptions.ConnectionError as e:
            # Узнаем имя возникшего исключения
            print(f'{bcolors.FAIL}{e.__class__.__name__}: {url}{bcolors.ENDC}')
            DataManager.__await(5)
            if(numLoad>5):
                return False
            else:
                return DataManager.__download(name, url, nameFile, numLoad + 1)
        except Exception as e:
            # Узнаем имя возникшего исключения
            print(f'{bcolors.FAIL}{e.__class__.__name__}: {url}{bcolors.ENDC}')
            DataManager.__await(3)
            if numLoad<=1:
               return DataManager.__download(name, url, nameFile, numLoad + 1)
            return False

        return DataManager.checkImage(imagePath, name);



    def __await(sec):
        '''
        Ожидание с выводом в консоль
        @sec - количество секунд
        '''
        for i in range(sec, 0, -1):
            print(f'Ждем: {i:03} s', end = '\r')
            time.sleep(1)
  

    def reinitIndexs(name):
        '''
        Изменение номеров файлов по порядку 0000, 0001 ...
        @name - запрос
        '''
        path = fm.getSourcesPath(name)
        jpg_files = os.listdir(path)
        digit_len = len(str(len(jpg_files)))
        
        # Создаём список файлов в папке
        initial_number = 0;
        # Перебираем каждый файл и увеличиваем порядковый номер
        for file_name in jpg_files:
            os.rename(path+'\\'+file_name, path + '\\' + f'tre_{initial_number}.jpg')
            initial_number += 1

        file_names = os.listdir(path)
        initial_number = 0;
        for file_name in file_names:
            indexName = str(initial_number).zfill(digit_len) + '.jpg'
            os.rename(path + '\\' + file_name, path + '\\' + indexName)
            initial_number+=1

    def openOrDelete(path):
        '''
        Проверяет возможность открытия файла как изображения, в случае невозможности открытия удаляет файл
        @path - путь к файлу
        @return - если файл не валиден, иначе изображение
        '''
        image = cv2.imread(path)
        if(image is None):
            os.remove(path)
            print(f'{bcolors.WARNING}Удалено невалидное изображение{bcolors.ENDC}')
        return image

    def resizeImage(image, path):
        '''
        Изменение размера изображения
        @image - загруженное изображение
        @query - текст запроса
        '''
        height = 128
        width = 128
        size = (width, height)
        image = cv2.resize(image, size)
        cv2.imwrite(path, image)
        return image

    def deleteIfExist(image, query, imagePath):
        '''
        Проверяет есть ли дубликаты изображения, если есть, удаляет файл
        @image - загруженное изображение
        @query - текст запроса
        @imagePath - ссылка на изображения
        @return - None, если файл не валиден, иначе изображение
        '''
        path = fm.getSourcesPath(query)
        file_names = os.listdir(path)
        for nameFile in file_names:
            filePath = f'{path}\\{nameFile}';
            if(imagePath == filePath):
                continue
            
            fileImage = cv2.imread(filePath)
            if((image == fileImage).all()):
                os.remove(imagePath)
                print(f'{bcolors.WARNING}Такое изображение уже загружено! Копия удалена{bcolors.ENDC}')
                return False
        return True

    def checkImage(path, query):
        '''
        Проверяет нужно ли это изображение, приводит к общему формату
        @param path - путь до изображения
        @param query - текст запроса
        @return True - изображение подходит, иначе False
        '''
        image = DataManager.openOrDelete(path)
        if image is None:
            return False
        image = DataManager.resizeImage(image, path)
        return DataManager.deleteIfExist(image, query, path)
        


