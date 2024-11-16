import unittest
from util.iterators import Iterator
class TestIterator(unittest.TestCase):

    def setUp(self):
        """Создание экземпляра итератора перед каждым тестом."""
        self.data = [1, 2, 3, 4, 5]
        self.iterator = Iterator(self.data)

    def test_iterate(self):
        """Тестируем итерацию по всем элементам."""
        result = []
        for item in self.iterator:
            result.append(item)

        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_next_method(self):
        """Тестируем метод next()"""
        self.assertEqual(self.iterator.next(), 1)
        self.assertEqual(self.iterator.next(), 2)
        self.assertEqual(self.iterator.next(), 3)
        self.assertEqual(self.iterator.next(), 4)
        self.assertEqual(self.iterator.next(), 5)
        self.assertIsNone(self.iterator.next())  # Достигли конца

    def test_prev_method(self):
        """Тестируем метод prev()"""
        self.iterator.next()  # Перемещаемся к 1
        self.iterator.next()  # Перемещаемся к 2
        self.assertEqual(self.iterator.prev(), 1)  # Возвращаемся к 1
        self.assertEqual(self.iterator.prev(), None)  # Впереди нет элемента

    def test_get_method(self):
        """Тестируем метод get()"""
        self.assertIsNone(self.iterator.get())  # В начале итератор
        self.iterator.next()
        self.assertEqual(self.iterator.get(), 1)  # Получаем текущее значение (1)
        self.iterator.next()
        self.assertEqual(self.iterator.get(), 2)  # Получаем текущее значение (2)

    def test_stop_iteration(self):
        """Тестируем StopIteration."""
        with self.assertRaises(StopIteration):
            while True: 
                next(self.iterator)

if __name__ == '__main__':
    unittest.main()




