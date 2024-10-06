from managers.DataManager import DataManager as dm
from managers.ConfigManager import ConfigManager as cm


def main():
    '''
    Функция точки входа в программу
    '''
    conf = cm()
    need_count = conf.image_count
    queries = conf.queries
    data = dm(conf)
    for query in queries:
        data.download_images(query, need_count)
        data.indexation(query)


if __name__ == '__main__':
    main()