import logging as log
from bs4 import BeautifulSoup



class ConfigManager:
    '''
    Класс отвечающий за конфигурацию проекта
    '''

    def __init__(self):
        with open('config.xml', 'r', encoding="utf-8") as fd:
            xml_file = fd.read()
            soup = BeautifulSoup(xml_file, 'lxml')
            config = soup.find('config')

            # получаем требования к изображению
            img = config.find('image')
            self.image_count = int(img['count'])
            self.image_size = (int(img['width']), int(img['height']))
            self.image_small = img['avatars'] == 'True'
            log.info('Нужно загружать миниатюры: %s', self.image_small)
            log.info('Приводить к размеру: %s', self.image_size)
            log.info('Необходимо скачать %d изображений', self.image_count)

            # получаем текст запросов
            self.queries = []
            queries = config.find('queries')
            self.need_upd = queries['need-update'] == 'True'
            for query in queries.findAll('query'):
                self.queries.append(query["text"])
            log.info('Запросы: %s', self.queries)

            # получаем настройки заголовка запроса и данные по умолчанию
            request = config.find('request')
            h = request.find('header')
            self.generate_header = h['generate-header'] == 'True'
            self.header = {}
            for item in h.findAll('default'):
                self.header[item['name']] = item.text

            #получаем пути приложения
            paths = config.find('paths')
            self.paths = {}
            for path in paths.findAll('path'):
                self.paths[path['name']] = path.text 
