from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QComboBox
from managers.FileManager import FileManager as fm
from util.Scripts import Script as scr

class  MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Анализатор"
        self.resize(300, 250)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('app/sources/logo.jpg'))
        window = QWidget()
        vbox = QVBoxLayout()
        self.image_view = QLabel()
        img = QPixmap('app/sources/logo.jpg')
        self.image_view.setPixmap(img)

        self.annots = fm.get_annotations();

        box_select= QHBoxLayout()
        self.cb_annot = QComboBox()
        ann = ['no'] + self.annots
        self.cb_annot.addItems(ann)
        box_select.addWidget(self.cb_annot)
        btn_open = QPushButton("Загрузить")
        btn_open.clicked.connect(self.btn_open_click)
        box_select.addWidget(btn_open)

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
        vbox.addWidget(self.image_view)
        vbox.addLayout(box_nav)

        window.setLayout(vbox)
        self.setCentralWidget(window)

    def btn_open_click(self):
        annot = self.cb_annot.currentText()
        if annot == 'no':
           return

        path_annot = f'{fm.create_annotation_folder()}//{annot}'
        self.iters = scr.get_iters_from_annotations(path_annot)
        tags = ['no'] + list(self.iters.keys()) 
        self.cb_tag.clear()
        self.cb_tag.addItems(tags)

    def btn_next_click(self):
        tag = self.cb_tag.currentText()
        if tag == 'no' or tag == '':
            return
        
        it = self.iters[tag]
        path = it.next();
        if not path:
            print('Достигли конца')

        img = QPixmap(path)
        self.image_view.setPixmap(img)

    def btn_prev_click(self):
        tag = self.cb_tag.currentText()
        if tag == 'no' or tag == '':
            return

        it = self.iters[tag]
        path = it.next();
        if not path:
            print('Достигли конца')

        img = QPixmap(path)
        self.image_view.setPixmap(img)

    def on_combobox_changed(self, value):
        if value == 'no'  or value == '':
            img = QPixmap('app/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return
        
        it = self.iters[value]
        path = it.get();
        if not path:
            img = QPixmap('app/sources/logo.jpg')
            self.image_view.setPixmap(img)
            return

        img = QPixmap(path)
        self.image_view.setPixmap(img)