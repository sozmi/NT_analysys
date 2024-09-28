
from managers.DataManager import DataManager as dm

def main():
    queries = ["polar bear","brown bear"]
    needCount = 1000
    for query in queries:
        while True:
            if(dm.clearData(query)>=needCount):
                break
            dm.downloadFound(query,needCount);
              

if __name__ == '__main__':
    main()