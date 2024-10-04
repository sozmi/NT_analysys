from email.mime import image
from managers.DataManager import DataManager as dm
from bs4 import BeautifulSoup

def main():
    fd = open('config.xml', 'r')
    xml_file = fd.read() 
    soup = BeautifulSoup(xml_file, 'lxml')
    config = soup.find('config')
    need_count = int(config.find('image')['count'])
    queries = []
    q = config.find('queries')
    for query in q.findAll('query'):
        queries.append(query["text"])

    print(f'Необходимо скачать {need_count} изображений по запросам: {queries}')
                   
    for query in queries:
        dm.downloadImages(query, need_count);
        dm.reinitIndexs(query)
              

if __name__ == '__main__':
    main()