import unittest
from util.scripts import get_keys_from_dict

class TestGetKeysFromDict(unittest.TestCase):

    def test_empty_dict(self):
        self.assertEqual(get_keys_from_dict({}), [])

    def test_single_key_dict(self):
        self.assertEqual(get_keys_from_dict({'a': 1}), ['a'])

    def test_multiple_key_dict(self):
        self.assertEqual(get_keys_from_dict({'a': 1, 'b': 2, 'c': 3}), ['a', 'b', 'c'])

    def test_dict_with_non_string_keys(self):
        # Тест с ключами разных типов
        self.assertEqual(get_keys_from_dict({1: 'a', 2: 'b'}), [1, 2])
        self.assertEqual(get_keys_from_dict({(1, 2): 'a'}), [(1, 2)])
        self.assertEqual(get_keys_from_dict({True: 'a'}), [True])  # True - bool

    def test_dict_with_nested_dict(self):
      # Тест со вложенными словарями. В данном случае, ожидается вывести все ключи первого уровня.
        nested_dict = {'a': 1, 'b': {'c': 2, 'd': 3}}
        self.assertEqual(get_keys_from_dict(nested_dict), ['a', 'b'])

    def test_input_not_dict(self):
      with self.assertRaises(AttributeError): #Проверяем, что функция обрабатывает не словарь как ошибку
          get_keys_from_dict(123) # Число
          get_keys_from_dict("строка") # Строка
          get_keys_from_dict([1, 2, 3]) # Список


if __name__ == '__main__':
    unittest.main()



