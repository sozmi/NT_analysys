import requests
from bs4 import BeautifulSoup

class ProxyManager(object):
    def __fill_proxy_list(self):
        #, 'https://www.sslproxies.org'
        urls = ['https://free-proxy-list.net']
        for url in urls:
            print(f'Начата загрузка прокси с ресурса: {url}')
            page = requests.get(url, timeout=(1, 2))
            
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
                proxy = 'http'
                if td[https_index].text=='yes': 
                    proxy +='s'
                proxy += f'://{td[ip_index].text}:{td[port_index].text}'
                self.proxies.add(proxy)
            print(f'Количество прокси:{len(self.proxies)}')


    def __init__(self):
        self.proxies = set([''])
        self.__fill_proxy_list()
        self.counter = -1
        self.proxies = list(self.proxies)


    def get_next(self):
        if self.counter>=len(self.proxies):
            self.counter = -1
        
        self.counter+=1
        return self.proxies[self.counter]

    def delete(self):
        self.proxies.pop(self.counter)
        print('delete')



