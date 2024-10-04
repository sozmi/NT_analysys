from bs4 import BeautifulSoup
from logger.Logger import Logger as l

class ConfigManager(object):
    need_count = 0
    queries = []
    def __init__(self):
        with open('config.xml', 'r') as fd:
            xml_file = fd.read() 
            soup = BeautifulSoup(xml_file, 'lxml')
            config = soup.find('config')
            ConfigManager.need_count = int(config.find('image')['count'])
            q = config.find('queries')
            for query in q.findAll('query'):
                ConfigManager.queries.append(query["text"])
            
            l.printInfo(f'Необходимо скачать {ConfigManager.need_count} изображений по запросам: {ConfigManager.queries}')




