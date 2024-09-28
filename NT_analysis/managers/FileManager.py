import os

class FileManager:
    '''
    Класс, отвечает за сохранение структуры и информации в программе
    '''

    def __getSystemsPath(name):
        '''
        Получает путь к системным данным
        @name - наименование(запрос) датасета
        @return - путь к системным данным
        '''
        path = FileManager.__createDSFolder(name)
        return FileManager.__createFolder(path + f'\\__systems')
    
    def __createDSFolder(name):
        '''
        Создает папку "\dataset\name"
        @name - наименование(запрос) датасета
        @return - путь к папке датасета
        '''
        path = f'{FileManager.__createDataFolder()}\\datasets\\{name}'
        return FileManager.__createFolder(path)

    def __createDataFolder():
        '''
        Создает папку с информацией, необходимой для работы приложения
        @return - путь к папке с данными
        '''
        path = f'data'
        return FileManager.__createFolder(path)

    def __createFolder(path):
        '''
        Создает папки по адресу
        @path - путь к папке
        @return - путь к папке
        '''
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def getUsedUrlPath(name):
        '''
        Получает путь к файлу, хранящему списку ссылок, которые были обработаны в рамках запроса
        @name - наименование(запрос) датасета
        @return - путь к файлу с url
        '''
        return FileManager.__getSystemsPath(name) + f'\\url.txt'

    def getPagePath(name):
        '''
        Получает путь к файлу, хранящему значение последней загруженной страницы
        @name - наименование(запрос) датасета
        @return - путь к файлу с информацией о странице
        '''
        return FileManager.__getSystemsPath(name) + f'\\page.txt'

    def getSourcesPath(name):
        '''
        Получает путь к папке с исходниками изображений
        @name - наименование(запрос) датасета
        @return - путь к файлу с ресурсами
        '''
        path = FileManager.__createDSFolder(name)
        return FileManager.__createFolder(path + f'\\sources')

    def getLastPage(name):
        '''
        Получает последнюю скачанную страницу для запроса
        @name - наименование(запрос) датасета
        @return - номер последней страницы
        '''
        path = FileManager.getPagePath(name)
        pageCount = 0
        if os.path.exists(path):
            with open(path, 'r') as file:
                pageCount = int(file.read()) + 1
        return pageCount

    def getUsedUrl(name):
        '''
        Получает список обработанных ссылок на изображения
        @name - наименование(запрос) датасета
        @return - номер
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


