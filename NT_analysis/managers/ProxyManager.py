from time import time
import requests
from bs4 import BeautifulSoup
from logger.Logger import Logger as l


class ProxyManager:
    '''
    Класс осуществляющий управление списком прокси
    '''

    def __init__(self):
        self.proxies = [{'http': ''}]
        self.__fill_proxy_list()
        self.counter = -1
        self.proxies = list(self.proxies)

    def __fill_proxy_list(self):
        '''
        Заполнение списка прокси из ресурсов
        '''
        urls = ['https://free-proxy-list.net', 'https://www.sslproxies.org']
        for url in urls:
            print(f'Начата загрузка прокси с ресурса: {url}')
            page = None
            while page is None:
                try:
                    page = requests.get(url, timeout=(3, 5))
                except Exception as e:
                    # Узнаем имя возникшего исключения
                    l.print_e(f'{e.__class__.__name__}: {url}')
                    for s in range(5, 0, -1):
                        print(f'Ждем: {s:03} с', end='\r')
                        time.sleep(1)

            root = BeautifulSoup(page.content, 'html.parser')
            table = root.find(
                'table', class_='table table-striped table-bordered')
            rows = table.findAll('tr')

            col = [row.text for row in rows[0].find_all('th')]
            https_index = col.index('Https')
            ip_index = col.index('IP Address')
            port_index = col.index('Port')
            rows.pop(0)

            for row in rows:
                td = row.find_all('td')
                scheme = 'https' if 'https' in td[https_index].text else 'http'
                proxy = f'{scheme}://{td[ip_index].text}:{td[port_index].text}'
                self.proxies.append({scheme: proxy})
            print(f'Количество прокси:{len(self.proxies)}')

    def get(self):
        '''
        Получение элемента на текущей позиции счетчика
        '''
        return self.proxies[self.counter]

    def get_next(self):
        '''
        Получение следующего элемента в списке, в случае окончания идем на второй круг
        '''
        if self.counter >= len(self.proxies)-1:
            self.counter = -1

        self.counter += 1
        return self.proxies[self.counter]
