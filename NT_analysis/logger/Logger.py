from logger.BColors import bcolors as c

class Logger(object):
    '''
    Класс отвечающий за информирование о процессе работы программы
    '''

    def printInfo(text):
        '''
        Вывод фоновой информации
        @text - текст для форматирования
        '''
        print(text)

    def printErr(text):
        '''
        Вывод ошибок
        @text - текст для форматирования
        '''
        print(c.FAIL + text + c.ENDC)

    def printWarn(text):
        '''
        Вывод предупреждений
        @text - текст для форматирования
        '''
        print(c.WARNING + text + c.ENDC)

    def printGood(text):
        '''
        Вывод успешности всей операции
        @text - текст для форматирования
        '''
        print(c.OKGREEN + text + c.ENDC)

    def printSubGood(text):
        '''
        Вывод успешности подоперации
        @text - текст для форматирования
        '''
        print(c.OKCYAN + text + c.ENDC)





