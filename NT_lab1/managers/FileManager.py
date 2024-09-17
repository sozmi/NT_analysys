import os

class FileManager:

    def __getSystemsPath(name):
        path = FileManager.__createDSFolder(name)
        return FileManager.__createFolder(path + f'\\__systems')

    def getUsedUrlPath(name):
        return FileManager.__getSystemsPath(name) + f'\\url.txt'

    def getPagePath(name):
        return FileManager.__getSystemsPath(name) + f'\\page.txt'

    def getSourcesPath(name):
        path = FileManager.__createDSFolder(name)
        return FileManager.__createFolder(path + f'\\sources')
    
    def getSmallPath(name):
        path = FileManager.__createDSFolder(name)
        return FileManager.__createFolder(path + f'\\small_sources')

    def getLastPage(name):
        path = FileManager.getPagePath(name)
        pageCount = 0
        if os.path.exists(path):
            with open(path, 'r') as file:
                pageCount = int(file.read()) + 1
        return pageCount

    def getUsedUrl(name):
         path = FileManager.getUsedUrlPath(name)
         usedURL = []
         if os.path.exists(path):
            with open(path, 'r') as file:
                usedURL = file.read().split('\n')
         return usedURL

    def saveLastPage(name, page):
        path = FileManager.getPagePath(name)
        with open(path, 'w') as file:
            file.write(str(page))

    def __createDSFolder(name):
        path = f'datasets\\{name}'
        if not os.path.isdir(path):
            os.makedirs(path)
        return path
    
    def __createFolder(path):
        if not os.path.isdir(path):
            os.makedirs(path)
        return path
