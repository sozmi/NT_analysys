from collections import defaultdict

from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget, QComboBox, QFileDialog

from util.scripts import copy_dataset_to_tag as copy_ds_tags, create_folder
from util.scripts import copy_dataset_to_rand as copy_ds_rand
from util.scripts import get_iters_from_annotations as get_iters



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

        box_select= QHBoxLayout()
        self.cb_annot = QComboBox()
        ann = ['no'] + self.annots
        self.cb_annot.addItems(ann)
        box_select.addWidget(self.cb_annot)
        btn_open = QPushButton("Загрузить")
        btn_open.clicked.connect(self.btn_open_click)
        box_select.addWidget(btn_open)

        box_create= QHBoxLayout()
        btn_create_rand = QPushButton("Создать датасет(случайная нумерация)")
        btn_create_rand.clicked.connect(self.btn_create_rand)
        btn_create_tag = QPushButton("Создать датасет(по тэгам)")
        btn_create_tag.clicked.connect(self.btn_create_tag)
        box_create.addWidget(btn_create_rand)
        box_create.addWidget(btn_create_tag)

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
