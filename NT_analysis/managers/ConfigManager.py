from bs4 import BeautifulSoup
from util.Logger import Logger as l


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

            # получаем текст запросов
            self.queries = []
            queries = config.find('queries')
            for query in queries.findAll('query'):
                self.queries.append(query["text"])

            # получаем настройки заголовка запроса и данные по умолчанию
            request = config.find('request')
            h = request.find('header')
            self.generate_header = h['generate-header'] == 'True'
            self.header = {}
            for item in h.findAll('default'):
                self.header[item['name']] = item.text

            l.print_i(f'Необходимо скачать {self.image_count} изображений по запросам: {self.queries}')
