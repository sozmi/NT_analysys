from re import S
from bs4 import BeautifulSoup
from logger.Logger import Logger as l

class ConfigManager(object):
    '''
    Класс отвечающий за конфигурацию проекта
    '''

    def __init__(self):
        with open('config.xml', 'r') as fd:
            xml_file = fd.read() 
            soup = BeautifulSoup(xml_file, 'lxml')
            config = soup.find('config')

            img = config.find('image')
            self.image_count = int(img['count'])
            self.image_size = (int(img['width']), int(img['height']))
            self.image_small = True if img['avatars'] == 'True' else False

            self.queries = []
            queries = config.find('queries')
            for query in queries.findAll('query'):
                self.queries.append(query["text"])

            self.header = {}
            request = config.find('request')
            h = request.find('header')
            for item in h.findAll('default'):
                self.header[item['name']] = item.text

            self.generate_header = True if h['generate-header'] == 'True' else False
         
            l.printInfo(f'Необходимо скачать {self.image_count} изображений по запросам: {self.queries}')




