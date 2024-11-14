class Iterator():
    '''
    Класс-итератор для прохода по элементам
    '''

    def __init__(self, data):
        '''
        Инициализация пременных
        @data - список данных
        '''
        self.counter = -1
        self.data = data

    def __iter__(self):
        '''
        Получение итератора
        @return возвращаем итаратор
        '''
        return self

    def __next__(self):
        '''
        Переход к следующему элементу до вызова исключения
        @return возвращаем итаратор
        '''
        item = self.next()
        if item is None:
            raise StopIteration
        return item

    def prev(self):
        '''
        Переходим к предыдущему элементу
        @return В случае достижения первого элемента None, иначе сам элемент
        '''
        if self.counter < 0:
            return None

        if self.counter == 0:
            # если дошли до начала, нужно переместить текущую позицию на элемент влево
            self.counter -= 1
            return None

        self.counter -= 1
        return self.data[self.counter]

    def next(self):
        '''
        Переходим к следующему элементу
        @return В случае достижения последнего элемента None, иначе сам элемент
        '''
        if len(self.data) - 1 < self.counter:
            return None

        if len(self.data) - 1 == self.counter:
            # если дошли до начала, нужно переместить текущую позицию на элемент вправо
            self.counter += 1
            return None

        self.counter += 1
        return self.data[self.counter]

    def get(self):
        '''
        Получение текущего значения итератора
        '''
        if len(self.data) <= self.counter or self.counter<0:
            return None
        return self.data[self.counter]
