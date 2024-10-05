from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
from managers.FileManager import FileManager as fm
from managers.ConfigManager import ConfigManager as cm
from logger.Logger import Logger as l
import requests
import os
import time
import json
import cv2

class DataManager(object):
    '''
    Класс отвечает за получение и загрузку данных
    '''
    frp = FreeProxy(rand=True)
    lastProxies = {}
    blackProxy =[]
    config = cm(False)
    def __init__(self, config):
        self.config = config

    def downloadImages(self, name, need_сount):
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
            urls = self.__parsePage(page, query)
            actualUrl = list(set(urls) - set(usedURL))
            l.printInfo(f'Найдено {len(actualUrl)} urls')
            
            with open(fm.getUsedUrlPath(name), 'a') as file:
                for url in actualUrl:
                    nameFile = str(number_file) + '.jpg'
                    isLoaded = self.__download(name, url, nameFile, 0)
                    usedURL.append(url)
                    file.write(url+"\n")
                    if isLoaded == True:
                        number_file+=1
                        imagesCount+=1
            l.printSubGood(f'Загружено {imagesCount} изображений из {need_сount}')
            page+=1
            fm.saveLastPage(name,page)
        l.printGood(f'Все изображения {name} загружены')

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


    def __getHtml(self, page, query, needProxy):
        '''
        Получение кода html страницы
        @page - номер страницы
        @query - запрос
        @needProxy - нужно ли использовать прокси при подключении
        '''
        URL = f'https://yandex.ru/images/touch/search?from=tabbar&p={page}&text={query}&itype=jpg'
        HEADERS = self.__getHeaders()
        proxies = self.lastProxies
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
                    l.printErr(e.__class__.__name__ + ' при поиске прокси')  
                    DataManager.__await(5);
                    DataManager.lastProxies = ''
                    l.printSubGood(f'Очищен черный список прокси')
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

        l.printSubGood('Подключились')
        
        return response.content


    def __parsePage(self, page, query):
        '''
        Разбор кода html страницы
        @page - номер страницы
        @query - запрос
        '''
        content = self.__getHtml(page, query, False)
        #получаем содержимое страницы
        rootDiv = None
        while rootDiv is None:
            root = BeautifulSoup(content, 'html.parser')
            rootDiv = root.find('div', class_="Root", id=lambda x: x and x.startswith('ImagesApp-'))
            #проверка на капчу
            if(rootDiv is None):
                self.lastProxies = {}
                print(f'Капча на {page} странице.') 
                content = self.__getHtml(page, query, True)

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


    def __getHeaders(self):
         '''
         Получение случайного заголовка страницы
         '''
         headers = self.config.header
         if self.config.need_create_ua:
            ua = UserAgent()
            headers['User-Agent'] = ua.random

         return headers

    def __download(self, name, url, nameFile, numLoad):
        '''
        Скачивание изображения по ссылке
        @name - запрос
        @url - ссылка на изображение
        @nameFile - название файла
        @newLoad - индикатор первый ли вызов функции
        '''
        HEADERS = self.__getHeaders()
        path = fm.getSourcesPath(name);
        imagePath = path +'\\'+nameFile;
        try:
            with requests.get(url, headers = HEADERS, stream=True, timeout=(5,15)) as r:
                with open(imagePath, 'wb') as f:
                    f.write(r.content)
                    print(f'Скачан файл [{nameFile}]: {url}') 
        except requests.exceptions.SSLError as e:
            # Узнаем имя возникшего исключения
            l.printErr(f'{e.__class__.__name__}: {url}')
            return False
        except requests.exceptions.ConnectionError as e:
            # Узнаем имя возникшего исключения
            l.printErr(f'{e.__class__.__name__}: {url}')
            DataManager.__await(5)
            if(numLoad>5):
                return False
            else:
                return DataManager.__download(name, url, nameFile, numLoad + 1)
        except Exception as e:
            # Узнаем имя возникшего исключения
            l.printErr(f'{e.__class__.__name__}: {url}')
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
  

    def reinitIndexs(self, name):
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
            l.printWarn('Удалено невалидное изображение')
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
                l.printWarn('Такое изображение уже загружено! Копия удалена')
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
        


