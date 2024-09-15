
from DataManager import DataManager

def main():
    queries = ["polar bear","brown bear"]
    needCount = 1000
    for query in queries:
        while True:
            if(DataManager.clearData(query)>=needCount):
                break
            DataManager.downloadFound(query,needCount);
        
       

if __name__ == '__main__':
    main()