from util.BColors import BColors as c

class Logger():
    '''
    Класс отвечающий за информирование о процессе работы программы
    '''

    def print_i(text):
        '''
        Вывод фоновой информации
        @text - текст для форматирования
        '''
        print(text)

    def print_e(text):
        '''
        Вывод ошибок
        @text - текст для форматирования
        '''
        print(c.FAIL + text + c.ENDC)

    def print_w(text):
        '''
        Вывод предупреждений
        @text - текст для форматирования
        '''
        print(c.WARNING + text + c.ENDC)

    def print_g(text):
        '''
        Вывод успешности всей операции
        @text - текст для форматирования
        '''
        print(c.OKGREEN + text + c.ENDC)

    def print_sub_g(text):
        '''
        Вывод успешности подоперации
        @text - текст для форматирования
        '''
        print(c.OKCYAN + text + c.ENDC)
