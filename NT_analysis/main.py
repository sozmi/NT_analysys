from managers.DataManager import DataManager  as dm
from managers.ConfigManager import ConfigManager as cm


def main():     
    conf = cm()
    need_count = conf.need_count
    queries = conf.queries
    data = dm()
    for query in queries:
        data.downloadImages(query, need_count);
        dm.reinitIndexs(query)
              

if __name__ == '__main__':
    main()