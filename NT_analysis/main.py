from managers.ConfigManager import ConfigManager as cm
from managers.DataManager import DataManager as dm
from app.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication
import sys

def main():
    '''
    Функция точки входа в программу
    '''
    conf = cm()
    need_count = conf.image_count
    queries = conf.queries
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
    #data = dm(conf)
    #for query in queries:
    #    data.download_images(query, need_count)
    #    data.indexation(query)
    
    #data.save_new_dataset(queries)


if __name__ == '__main__':
    main()