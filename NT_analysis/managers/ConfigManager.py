from email import header
from urllib import request
from bs4 import BeautifulSoup
from logger.Logger import Logger as l

class ConfigManager(object):
    '''
    Класс отвечающий за конфигурацию проекта
    '''
    image_size = []
    need_count = 0
    queries = []
    need_create_ua = False
    header = {}

    def __init__(self, need_open=True):
        if not need_open:
            return
        with open('config.xml', 'r') as fd:
            xml_file = fd.read() 
            soup = BeautifulSoup(xml_file, 'lxml')
            config = soup.find('config')

            img = config.find('image')
            self.need_count = int(img['count'])
            self.image_size = (int(img['width']), int(img['height']))

            queries = config.find('queries')
            for query in queries.findAll('query'):
                self.queries.append(query["text"])

            request = config.find('request')
            h = request.find('header')
            for item in h.findAll('default'):
                self.header[item['name']] = item.text

            if h['isgenerationua'] == 'True':
                self.need_create_ua = True
         
            l.printInfo(f'Необходимо скачать {self.need_count} изображений по запросам: {self.queries}')




