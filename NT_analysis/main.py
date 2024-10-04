from email.mime import image
from managers.DataManager import DataManager  as dm
from managers.ConfigManager import ConfigManager as cm


def main():     
    conf = cm()
    need_count = conf.need_count
    queries = conf.queries
    for query in queries:
        dm.downloadImages(query, need_count);
        dm.reinitIndexs(query)
              

if __name__ == '__main__':
    main()