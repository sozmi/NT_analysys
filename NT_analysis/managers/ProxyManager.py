from time import time
import requests
from bs4 import BeautifulSoup
from logger.Logger import Logger as l

class ProxyManager(object):        
    def __fill_proxy_list(self):
        #, 'https://www.sslproxies.org'
        urls = ['https://free-proxy-list.net']
        for url in urls:
            print(f'Начата загрузка прокси с ресурса: {url}')
            page = None
            while page is None:
                try:
                    page = requests.get(url, timeout=(3, 5))
                except Exception as e:
                    # Узнаем имя возникшего исключения
                    l.printErr(f'{e.__class__.__name__}: {url}')
                    for i in range(5, 0, -1):
                        print(f'Ждем: {i:03} s', end = '\r')
                        time.sleep(1)

            
            root = BeautifulSoup(page.content, 'html.parser')    
            table = root.find('table', class_='table table-striped table-bordered')
            rows = table.findAll('tr')

            col = [j.text for j in rows[0].find_all('th')]
            https_index = col.index('Https')
            ip_index = col.index('IP Address')
            port_index = col.index('Port')
            rows.pop(0)

            for i in rows:
                td = i.find_all('td')
                scheme = 'https' if 'https' in td[https_index].text else 'http'
                proxy = f'{scheme}://{td[ip_index].text}:{td[port_index].text}'
                self.proxies.append({scheme : proxy})
            print(f'Количество прокси:{len(self.proxies)}')


    def __init__(self):
        self.proxies = [{'http':''}]
        self.__fill_proxy_list()
        self.counter = -1
        self.proxies = list(self.proxies)

    def get(self):
        return self.proxies[self.counter]

    def get_next(self):
        if self.counter>=len(self.proxies)-1:
            self.counter = -1
        
        self.counter+=1
        return self.proxies[self.counter]



