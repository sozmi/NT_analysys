from ast import Import
from collections import defaultdict

from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget, QComboBox, QFileDialog

from util.scripts import copy_dataset_to_tag as copy_ds_tags, create_folder
from util.scripts import copy_dataset_to_rand as copy_ds_rand
from util.scripts import get_iters_from_annotations as get_iters
from util.scripts import get_keys_from_dict as get_keys
from analysis import analysis as a
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox

class MessageDialog(QMessageBox):
    def __init__(self, info):
        super().__init__()
        self.setWindowTitle("Сообщение")
        self.setText("Статистика DataFrame:")
        self.setInformativeText(info)
        self.setStandardButtons(QMessageBox.Ok)

class MainWindow(QMainWindow):
    def __init__(self, fm):
        super(MainWindow, self).__init__()
        self.fm = fm
        self.title = "Анализатор"
        self.resize(300, 250)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('app/sources/logo.jpg'))
        self.iters = defaultdict(list);
        window = QWidget()
        vbox = QVBoxLayout()
        self.image_view = QLabel()
        img = QPixmap('app/sources/logo.jpg')
        self.image_view.setPixmap(img)

        self.annots = self.fm.get_annotations()

        box_select = QHBoxLayout()
        self.cb_annot = QComboBox()
        ann = ['no'] + self.annots
        self.cb_annot.addItems(ann)
        box_select.addWidget(self.cb_annot)
        btn_open = QPushButton("Загрузить")
        btn_open.clicked.connect(self.btn_open_click)
        box_select.addWidget(btn_open)

        box_create = QHBoxLayout()
        btn_create_rand = QPushButton("Создать датасет(случайная нумерация)")
        btn_create_rand.clicked.connect(self.btn_create_rand)
        btn_create_tag = QPushButton("Создать датасет(по тэгам)")
        btn_create_tag.clicked.connect(self.btn_create_tag)
        box_create.addWidget(btn_create_rand)
        box_create.addWidget(btn_create_tag)

        box_anal = QHBoxLayout()
        btn_stat = QPushButton("Статистика")
        btn_stat.clicked.connect(self.btn_stat_click)
        btn_count = QPushButton("Количество пикселей")
        btn_count.clicked.connect(self.btn_count_click)
        btn_gist = QPushButton("Гистограмма по каналам")
        btn_gist.clicked.connect(self.btn_gist_click)
        box_anal.addWidget(btn_stat)
        box_anal.addWidget(btn_count)
        box_anal.addWidget(btn_gist)

        box_nav = QHBoxLayout()
        prev_btn = QPushButton("Предыдущее изображение")
        prev_btn.clicked.connect(self.btn_prev_click)
        box_nav.addWidget(prev_btn)
        self.cb_tag = QComboBox()
        self.cb_tag.currentTextChanged.connect(self.on_combobox_changed)
        box_nav.addWidget(self.cb_tag)
        next_btn = QPushButton("Следующее изображение")
        next_btn.clicked.connect(self.btn_next_click)
        box_nav.addWidget(next_btn)

        vbox.addLayout(box_select)
        vbox.addLayout(box_create)
        vbox.addLayout(box_anal)
        vbox.addWidget(self.image_view)
        vbox.addLayout(box_nav)

        window.setLayout(vbox)
        self.setCentralWidget(window)


    def btn_create_tag(self):
        path_ann, _ = QFileDialog.getOpenFileName(None, 'Выберите файл исходной аннотации')
        path_to = create_folder(f'{self.fm.path_copy}\\tag')
        ann = copy_ds_tags(path_to, path_ann, self.fm.path_ann)
        self.cb_annot.addItem(ann)        

    def btn_create_rand(self):
        path_ann, _ = QFileDialog.getOpenFileName(None, 'Выберите файл исходной аннотации')
        path_to = create_folder(f'{self.fm.path_copy}\\rand')
        ann = copy_ds_rand(path_to, path_ann, self.fm.path_ann)
        self.cb_annot.addItem(ann)


    def btn_open_click(self):
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return

        path_annot = f'{self.fm.create_annotation_folder()}\\{annot}'
        self.iters = get_iters(path_annot)
        tags = ['no'] + list(self.iters.keys()) 
        self.cb_tag.clear()
        self.cb_tag.addItems(tags)

    def btn_next_click(self):
        tag = self.cb_tag.currentText()
        if tag == 'no' or tag == '':
            return
        it = self.iters[tag]
        path = it.next()
        if not path:
            print('Достигли конца')
            img = QPixmap('app/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return

        img = QPixmap(path)
        self.image_view.setPixmap(img)

    def btn_prev_click(self):
        tag = self.cb_tag.currentText()
        if tag == 'no' or tag == '':
            return

        it = self.iters[tag]
        path = it.prev()
        if not path:
            print('Достигли конца')
            img = QPixmap('app/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return

        img = QPixmap(path)
        self.image_view.setPixmap(img)

    def on_combobox_changed(self, value):
        if value == 'no'  or value == '':
            img = QPixmap('app/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return
        it = self.iters[value]
        path = it.get()
        if not path:
            img = QPixmap('app/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return

        img = QPixmap(path)
        self.image_view.setPixmap(img)

    def btn_stat_click(self):
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return

        path = f'{self.fm.create_annotation_folder()}\\{annot}'
        df = a.annotation_to_frame(path,['polar bear', 'brown bear'])
        print(df)
        df = a.statistic(df)
        dialog = MessageDialog(df)
        dialog.exec_()

    def btn_count_click(self):
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return

        path = f'{self.fm.create_annotation_folder()}\\{annot}'
        df = a.annotation_to_frame(path, get_keys(self.iters))
        df = a.count_pixels_for_group(df)
        dialog = MessageDialog(df)
        dialog.exec_()

    def btn_gist_click(self):
        annot = self.cb_annot.currentText()
        if annot == 'no':
            return

        path = f'{self.fm.create_annotation_folder()}\\{annot}'
        df = a.annotation_to_frame(path, get_keys(self.iters))
        b,g,r  = a.compute_histogram(df, 0)
        a.plot_histograms(b,g,r)