import sys
import logging as log
from PySide6.QtWidgets import QApplication
from managers.FileManager import FileManager as fm
from managers.ConfigManager import ConfigManager as cm
from managers.DataManager import DataManager as dm
from app.ui.main_window import MainWindow

from util.formatter import CustomFormatter


def show_app(fman):
    '''
    Вызов графического интерфейса
    '''
    app = QApplication(sys.argv)
    w = MainWindow(fman)
    w.show()
    sys.exit(app.exec())

def init_logger():
    '''
    Настройки логгера
    '''
    logger = log.getLogger("NT_analysis")
    logger.setLevel(log.DEBUG)
    ch = log.StreamHandler()
    ch.setLevel(log.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

def update_dataset(conf, fman):
    '''Загрузка и обновление датасета'''
    need_count = conf.image_count
    queries = conf.queries

    data = dm(conf, fman)
    for query in queries:
        data.download_images(query, need_count)
        data.indexation(query)
    data.save_new_dataset(queries)

def main():
    '''
    Функция точки входа в программу
    '''
    init_logger()
    log.basicConfig(level= log.DEBUG)
    conf = cm()
    fman = fm(conf)
    if conf.need_upd:
        update_dataset(conf, fman)

    show_app(fman)

if __name__ == '__main__':
    main()
