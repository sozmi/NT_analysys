from managers.DataManager import DataManager  as dm
from managers.ConfigManager import ConfigManager as cm


def main():     
    conf = cm()
    need_count = conf.image_count
    queries = conf.queries
    data = dm(conf)
    for query in queries:
        data.downloadImages(query, need_count);
        data.reinitIndexs(query)
              

if __name__ == '__main__':
    main()