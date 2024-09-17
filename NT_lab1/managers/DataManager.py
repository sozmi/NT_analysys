from random import randint
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
import FileManager as fm

import matplotlib.pyplot as plt
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
    frp = FreeProxy(rand=True)
    lastProxies = {}
    blackProxy =[]
    
    def downloadFound(name, needCount):
        urls = []
        usedURL = fm.getUsedUrl(name)
        page = fm.getLastPage(name)
        number_file = len(usedURL)
        query = str.replace(name,' ','%20')
        
        path = fm.getSourcesPath(name)
        jpg_files = os.listdir(path)
        imagesCount = len(jpg_files)

        #ищем ссылки на оригинальные изображения
        while imagesCount < needCount: 
            urls = DataManager.__parsePage(page, query)
            actualUrl = list(set(urls) - set(usedURL))
            print(f'Find {len(actualUrl)} urls')
            
            with open(fm.getUsedUrlPath(name), 'a') as file:
                for url in actualUrl:
                    nameFile = 'download_' + str(number_file) + '.jpg'
                    isLoaded = DataManager.__download(name, url, nameFile, True)
                    usedURL.append(url)
                    file.write(url+"\n")
                    if isLoaded == True:
                        number_file+=1
                        imagesCount+=1
            print(f'{bcolors.OKCYAN} {imagesCount} images out of {needCount} {bcolors.ENDC} ')
            page+=1
            fm.saveLastPage(name,page)

    def __printInfoConnect(url, proxy, headers):
        if(len(proxy) == 0):
            proxy = 'no'

        print()
        print(f'URL: {url}')
        print(f'Proxy: {proxy}')
        print(f'Headers UA: {headers}')


    def __getHtml(page, query, needProxy):
        URL = f'https://yandex.ru/images/touch/search?from=tabbar&p={page}&text={query}&itype=jpg'
        HEADERS = DataManager.__getHeaders()
        proxies = DataManager.lastProxies
        proxy = ''
        if(needProxy):
            while len(proxies)==0:
                try:
                    proxy = DataManager.frp.get()
                    if(proxy in DataManager.blackProxy):
                        print(f'Proxy {proxy} in black list')
                        continue
                    proxies = { 'http': proxy, 'https': proxy }
                    DataManager.lastProxies = proxies
                except Exception as e:
                    # Узнаем имя возникшего исключения
                    print(e.__class__.__name__ + ' in find proxy')  
                    DataManager.__await(5);
                    DataManager.lastProxies = ''
    
        
        DataManager.__printInfoConnect(URL, proxies, HEADERS)

        try:
            response = requests.get(URL, headers=HEADERS, timeout=2, proxies=proxies, verify=False)
        except Exception as e:
            # Узнаем имя возникшего исключения
            print(e.__class__.__name__ + f': {URL}') 
            DataManager.lastProxies = ''
            DataManager.blackProxy.append(proxy)
            return DataManager.__getHtml(page, query, True)

        print('Connected')
        
        return response.content


    def __parsePage(page,query):
        content = DataManager.__getHtml(page, query, False)
        #получаем содержимое страницы
        rootDiv = None
        while rootDiv is None:
            root = BeautifulSoup(content, 'html.parser')
            rootDiv = root.find('div', class_="Root", id=lambda x: x and x.startswith('ImagesApp-'))
            #проверка на капчу
            if(rootDiv is None):
                DataManager.lastProxies = {}
                print(f'Capcha on {page} page.') 
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
         ua = UserAgent(os='windows',min_percentage=40)
         headers = {'User-Agent': ua.random,
                   'Accept-Encoding': 'gzip, deflate, br, zstd',
                   'Accept-Language': 'ru,en;q=0.9',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
                   }
         return headers


    def __download(name, url, nameFile, newLoad):
        HEADERS = DataManager.__getHeaders()
        path = fm.getSourcesPath(name);
        try:
            with requests.get(url, headers=HEADERS, stream=True, timeout=(5,15)) as r:
                with open(path +'\\'+nameFile, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    print(f'Download file[{nameFile}]: {url}')
                    return True
        except requests.exceptions.SSLError as e:
            # Узнаем имя возникшего исключения
            print(e.__class__.__name__ + f': {url}')
            return False
        except Exception as e:
            # Узнаем имя возникшего исключения
            print(e.__class__.__name__ + f': {url}')
            DataManager.__await(randint(1,5))
            if(newLoad == True):
               return DataManager.__download(name, url, nameFile, False)
        return False


    def __await(sec):
        for i in range(sec, 0, -1):
            print(f'Sleep: {i:03} s', end = '\r')
            time.sleep(1)
  

    def reinitIndexs(name):
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


    def removeUnunique(name):
        path = fm.getSourcesPath(name)
        if not os.path.isdir(path):
            return 0
        count = 0
        file_names = os.listdir(path)
        return len(file_names)
        for nameA in file_names:
            image_1 = cv2.imread(f'{path}\\{nameA}')

            for nameB in file_names:
                if(nameA == nameB):
                    continue
                image_2 = cv2.imread(f'{path}\\{nameB}')
                if(image_1 == image_2):
                    os.remove(f'{path}\\{nameB}')
                    count+=1
        print(f'Deleted {count} ununique files')
        return len(file_names);

    def removeUnvalide(name):
        path = fm.getSourcesPath(name)
        if not os.path.isdir(path):
            return
        count = 0
        file_names = os.listdir(path)
        for name in file_names:
            image = cv2.imread(f'{path}\\{name}')
            if(image is None):
                os.remove(f'{path}\\{name}')
                count+=1
        print(f'Deleted {count} unvalide files')
     
    
    def resizeImages(name):
        height = 128
        width = 128
        size = (width, height)
        path = fm.getSourcesPath(name)
        smallP = fm.getSmallPath(name)

        files_small = os.listdir(smallP)
        for sname in files_small:
            os.remove(f'{smallP}\\{sname}')

        file_names = os.listdir(path)
        for fname in file_names:
            img = cv2.imread(path+f'\\{fname}')
            dst = cv2.resize( img, size )
            cv2.imwrite(smallP + f'\\{fname}', dst)


    def clearData(name):
        print(f'Start cleaning data {name}...')
        print('Remove unvalide files...')
        DataManager.removeUnvalide(name)
        print('Remove non-unique files...')
        count = DataManager.removeUnunique(name)
        print('Update indexs')
        DataManager.reinitIndexs(name)
        DataManager.resizeImages(name)
        return count

