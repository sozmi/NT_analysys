import os

class FileManager:
    '''
    Класс, отвечает за сохранение структуры и информации в программе
    '''

    def get_systems_path(name):
        '''
        Получает путь к системным данным
        @name - наименование(запрос) датасета
        @return - путь к системным данным
        '''
        path = FileManager.create_ds_folder(name)
        return FileManager.create_folder(path + '\\__systems')

    def get_ds_folder():
        '''
        Создает папку "\\dataset"
        @name - наименование(запрос) датасета
        @return - путь к папке датасета
        '''
        path = f'{FileManager.create_data_folder()}\\datasets'
        return FileManager.create_folder(path)

    def create_ds_folder(name):
        '''
        Создает папку "\\dataset\\name"
        @name - наименование(запрос) датасета
        @return - путь к папке датасета
        '''
        path = f'{FileManager.create_data_folder()}\\datasets\\{name}'
        return FileManager.create_folder(path)
    
    def create_annotation_folder():
        '''
        Создает папку "\\annotation"
        @return - путь к папке c аннотациями
        '''
        path = f'{FileManager.create_data_folder()}\\annotation'
        return FileManager.create_folder(path)

    def create_data_folder():
        '''
        Создает папку с информацией, необходимой для работы приложения
        @return - путь к папке с данными
        '''
        path = 'data'
        return FileManager.create_folder(path)

    def create_folder(path):
        '''
        Создает папки по адресу
        @path - путь к папке
        @return - путь к папке
        '''
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def get_used_url_path(name):
        '''
        Получает путь к файлу, хранящему списку ссылок, которые были обработаны в рамках запроса
        @name - наименование(запрос) датасета
        @return - путь к файлу с url
        '''
        return FileManager.get_systems_path(name) + '\\url.txt'
    
    def get_annotation_path(name):
        '''
        Получает путь к файлу, хранящему значение последней загруженной страницы
        @name - наименование(запрос) датасета
        @return - путь к файлу с информацией о странице
        '''
        return FileManager.get_systems_path(name) + '\\annotation.csv'

    def get_page_path(name):
        '''
        Получает путь к файлу, хранящему значение последней загруженной страницы
        @name - наименование(запрос) датасета
        @return - путь к файлу с информацией о странице
        '''
        return FileManager.get_systems_path(name) + '\\page.txt'

    def get_sources_path(name):
        '''
        Получает путь к папке с исходниками изображений
        @name - наименование(запрос) датасета
        @return - путь к файлу с ресурсами
        '''
        path = FileManager.create_ds_folder(name)
        return FileManager.create_folder(path + '\\sources')

    def get_used_url(name):
        '''
        Получает список обработанных ссылок на изображения
        @name - наименование(запрос) датасета
        @return - список ссылок
        '''
        path = FileManager.get_used_url_path(name)
        urls = []
        if os.path.exists(path):
            with open(path, 'r', encoding="utf-8") as file:
                urls = file.read().split('\n')
        return urls

    def save_last_page(name, page):
        '''
        Сохраняет последнюю скачанную страницу
        @name - наименование(запрос) датасета
        @page - номер страницы
        '''
        path = FileManager.get_page_path(name)
        with open(path, 'w', encoding="utf-8") as file:
            file.write(str(page))

    def get_last_page(name):
        '''
        Получает последнюю скачанную страницу для запроса
        @name - наименование(запрос) датасета
        @return - номер последней страницы
        '''
        path = FileManager.get_page_path(name)
        count_page = 0
        if os.path.exists(path):
            with open(path, 'r', encoding="utf-8") as file:
                count_page = int(file.read()) + 1
        return count_page

    def get_annotations():
        '''
        Получает список аннотаций
        '''
        path = FileManager.create_annotation_folder()
        return os.listdir(path)