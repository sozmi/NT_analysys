import os

class FileManager:
    '''
    Класс, отвечает за сохранение структуры и информации в датасете
    '''

    def __getSystemsPath(name):
        '''
        получает путь к системным данным
        @name - наименование(запрос) датасета
        '''
        path = FileManager.__createDSFolder(name)
        return FileManager.__createFolder(path + f'\\__systems')

    def getUsedUrlPath(name):
        '''
        получает путь к файлу, хранящему списку ссылок, которые были обработаны в рамках запроса
        @name - наименование(запрос) датасета
        '''
        return FileManager.__getSystemsPath(name) + f'\\url.txt'

    def getPagePath(name):
        '''
        получает путь к файлу, хранящему значение последней загруженной страницы
        @name - наименование(запрос) датасета
        '''
        return FileManager.__getSystemsPath(name) + f'\\page.txt'

    def getSourcesPath(name):
        '''
        получает путь к папке с исходниками изображений
        @name - наименование(запрос) датасета
        '''
        path = FileManager.__createDSFolder(name)
        return FileManager.__createFolder(path + f'\\sources')
    
    def getSmallPath(name):
        '''
        получает путь к папке с сжатыми изображениями
        @name - наименование(запрос) датасета
        '''
        path = FileManager.__createDSFolder(name)
        return FileManager.__createFolder(path + f'\\small_sources')

    def getLastPage(name):
        '''
        получает последнюю скачанную страницу для запроса
        @name - наименование(запрос) датасета
        '''
        path = FileManager.getPagePath(name)
        pageCount = 0
        if os.path.exists(path):
            with open(path, 'r') as file:
                pageCount = int(file.read()) + 1
        return pageCount

    def getUsedUrl(name):
        '''
        получает список обработанных ссылок на изображения
        @name - наименование(запрос) датасета
        '''
        path = FileManager.getUsedUrlPath(name)
        usedURL = []
        if os.path.exists(path):
            with open(path, 'r') as file:
                usedURL = file.read().split('\n')
        return usedURL

    def saveLastPage(name, page):
        '''
        сохраняет последнюю скачанную страницу
        @name - наименование(запрос) датасета
        '''
        path = FileManager.getPagePath(name)
        with open(path, 'w') as file:
            file.write(str(page))

    def __createDSFolder(name):
        '''
        создает папку dataset/name
        @name - наименование(запрос) датасета
        '''
        path = f'datasets\\{name}'
        return FileManager.__createFolder(path)
    
    def __createFolder(path):
        '''
        создает папки по адресу
        @path - путь к папке
        '''
        if not os.path.isdir(path):
            os.makedirs(path)
        return path
