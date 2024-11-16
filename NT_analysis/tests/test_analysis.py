import unittest
import pandas as pd
from analysis import analysis as a
from unittest.mock import patch
from io import StringIO

class Test_analysis(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Создание фиктивного DataFrame для тестов."""
        data = {
            'height': [100, 200, 150, 300],
            'width': [50, 80, 75, 100],
            'depth': [0, 0, 0, 0],
            'label': ['A', 'B', 'A', 'B']
        }
        self.sample_df = pd.DataFrame(data)

    @patch('matplotlib.pyplot.show')  # Замена plt.show() на mock
    def test_statistic(self, mock_show):
        stats = a.statistic(self.sample_df)
        self.assertIn('count', stats)
        self.assertIn('mean', stats)
        self.assertIn('std', stats)
        self.assertIn('min', stats)
        self.assertIn('max', stats)

    def test_df_filter_1(self):
        filtered_df = a.df_filter_1(self.sample_df, 'A')
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all(filtered_df['label'] == 'A'))

    def test_df_filter_2(self):
        filtered_df = a.df_filter_2(self.sample_df, 'A', max_width=75, max_height=150)
        self.assertEqual(len(filtered_df), 2)
        self.assertEqual(filtered_df.iloc[0]['label'], 'A')
        self.assertLessEqual(filtered_df.iloc[0]['width'], 75)
        self.assertLessEqual(filtered_df.iloc[0]['height'], 150)

    def test_count_pixels_for_group(self):
        result = a.count_pixels_for_group(self.sample_df)
        
        # Преобразуем обратно в DataFrame для проверки
        result_df = pd.read_csv(StringIO(result), delim_whitespace=True)
        
        self.assertIn('label', result_df.columns)
        self.assertIn('max', result_df.columns)
        self.assertIn('min', result_df.columns)
        self.assertIn('mean', result_df.columns)
        self.assertEqual(len(result_df), 2)  # Должны быть 2 класса A и B

        # Проверка вычисленных значений пикселей
        self.assertEqual(result_df[result_df['label'] == 'A']['mean'].values[0], (100 * 50 + 150 * 75) / 2)
        self.assertEqual(result_df[result_df['label'] == 'B']['mean'].values[0], (200 * 80 + 300 * 100) / 2)

if __name__ == '__main__':
    unittest.main()
