import pandas as pd
import matplotlib.pyplot as plt 
import cv2

def annotation_to_frame(path_ann, list_tags):
    '''
    Получаем DataFrame из файла аннотации.
    @path_ann - путь к аннотации
    @list_tags - список тэгов. метка соответствует индексу в списке
    @return - сформированный dataframe
    '''
    df = pd.read_csv(path_ann, usecols=['absolute_path', 'tag'])
    df['label'] = df['tag'];
    for idx, x in enumerate(list_tags):
        df['label']=df['label'].replace(x, idx) 

    for _, row in df.iterrows():
        path = row['absolute_path']
        img = plt.imread(path)
        df['height'],df['width'], df['depth'] = img.shape  
       
    print(df.columns)
    return df

def statistic(df):
    stats = df[['height', 'width', 'depth', 'label']].describe().to_string()
    # Гистограмма по меткам
    label_counts = df['label'].value_counts()
    label_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.show()
    return stats

def df_filter_1(df, label):
    '''
    Фильтруем DataFrame по метке класса
    @df - входной DataFrame
    @label - метка класса для фильтрации
    @return отфильтрованный DataFrame
    '''
    return df[df['label'] == label]

def df_filter_2(df, label, max_width, max_height):
    '''
    Фильтрует DataFrame по заданным параметрам.
    @df - входной DataFrame
    @label - метка класса для фильтрации
    @max_width - максимальное значение ширины
    @max_height - максимальное значение высоты
    @return - отфильтрованный DataFrame
    '''
    filtered_df = df[
        (df['label'] == label) &
        (df['height'] <= max_height) &
        (df['width'] <= max_width)
    ]
    return filtered_df

def count_pixels_for_group(df):
    '''
    Считаем количество пикселей
    @df - входной DataFrame
    @return - отфильтрованный DataFrame с посчитанным количеством пикселей
    '''
    df['pixels'] = df['height'] * df['width']
    grouped_df = df.groupby('label')['pixels'].agg(['max', 'min', 'mean']).reset_index()
    return grouped_df.to_string()

def compute_histogram(df, class_label):
    # Случайный выбор изображения из DataFrame по метке класса
    df = df_filter_1(df, class_label)
    # Конвертация изображения в формат BGR (OpenCV)
    path = df.loc[df.sample().index, 'absolute_path'].to_numpy()[0]
    img = plt.imread(path)
    
    # Вычисление гистограммы для каждого канала
    hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
    hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])
    
    return hist_b, hist_g, hist_r

def plot_histograms(hist_b, hist_g, hist_r):
    # Отрисовка гистограмм
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 3, 1)
    plt.plot(hist_b, color='blue')
    plt.title('Гистограмма канала B')
    plt.xlabel('Интенсивность')
    plt.ylabel('Частота')
    
    plt.subplot(1, 3, 2)
    plt.plot(hist_g, color='green')
    plt.title('Гистограмма канала G')
    plt.xlabel('Интенсивность')
    plt.ylabel('Частота')

    plt.subplot(1, 3, 3)
    plt.plot(hist_r, color='red')
    plt.title('Гистограмма канала R')
    plt.xlabel('Интенсивность')
    plt.ylabel('Частота')

    plt.tight_layout()
    plt.show()




