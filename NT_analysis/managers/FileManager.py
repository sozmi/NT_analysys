import os
from util.scripts import create_folder

class FileManager:
    '''
    Класс, отвечает за сохранение структуры и информации в программе
    '''

    def __init__(self, config):
        '''
        Конструктор путей приложения
        @config - конфигурационный файл приложения
        '''
        self.path_dst = config.paths["datasets"]
        create_folder(self.path_dst)

        self.path_sys = config.paths["systems"]
        create_folder(self.path_sys)

        self.path_ann = config.paths["annotations"]
        create_folder(self.path_ann)

        self.path_copy = config.paths["copy_to"]
        create_folder(self.path_copy)
    
    def create_annotation_folder(self):
        '''
        Создает папку "\\annotation"
        @return - путь к папке c аннотациями
        '''
        return self.path_ann

    def path_used_url(self, name):
        '''
        Получает путь к файлу, хранящему списку ссылок, которые были обработаны в рамках запроса
        @name - наименование(запрос) датасета
        @return - путь к файлу с url
        '''
        return self.path_sys + f'\\{name}.urls'
    
    def get_path_ann(self, name):
        '''
        Получает путь к файлу, хранящему аннотацию датасета
        @name - наименование(запрос) датасета
        @return - путь к файлу с информацией о странице
        '''
        return self.get_sources_path(name) + '\\info.csv'

    def path_page(self, name):
        '''
        Получает путь к файлу, хранящему значение последней загруженной страницы
        @name - наименование(запрос) датасета
        @return - путь к файлу с информацией о странице
        '''
        return self.path_sys + f'\\{name}.page'

    def get_sources_path(self, name):
        '''
        Получает путь к папке с исходниками изображений
        @name - наименование(запрос) датасета
        @return - путь к файлу с ресурсами
        '''
        path = self.path_dst + f'\\{name}'
        return create_folder(path)

    def used_urls(self, name):
        '''
        Получает список обработанных ссылок на изображения
        @name - наименование(запрос) датасета
        @return - список ссылок
        '''
        path = self.path_used_url(name)
        urls = []
        if os.path.exists(path):
            with open(path, 'r', encoding="utf-8") as file:
                urls = file.read().split('\n')
        return urls

    def save_last_page(self, name, page):
        '''
        Сохраняет последнюю скачанную страницу
        @name - наименование(запрос) датасета
        @page - номер страницы
        '''
        path = self.path_page(name)
        with open(path, 'w', encoding="utf-8") as file:
            file.write(str(page))

    def last_page(self, name):
        '''
        Получает последнюю скачанную страницу для запроса
        @name - наименование(запрос) датасета
        @return - номер последней страницы
        '''
        path = self.path_page(name)
        count_page = 0
        if os.path.exists(path):
            with open(path, 'r', encoding="utf-8") as file:
                count_page = int(file.read()) + 1
        return count_page

    def get_annotations(self):
        '''
        Получает список аннотаций
        '''
        path = self.create_annotation_folder()
        return os.listdir(path)