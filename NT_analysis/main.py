
from managers.DataManager import DataManager as dm
import shutil
import requests

def main():
    queries = ["polar bear","brown bear"]
    needCount = 1000
                   
    for query in queries:
        dm.downloadImages(query, needCount);
        dm.reinitIndexs(query)
              

if __name__ == '__main__':
    main()