from email.mime import image
import sys
import PySide6
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QComboBox

class  MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Анализатор"
        self.resize(300, 250)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('app/sources/logo.jpg'))
        window = QWidget()
        vbox = QVBoxLayout()
        image_view = QLabel()
        img = QPixmap('app/sources/logo.jpg')
        image_view.setPixmap(img)

        box_select= QHBoxLayout()
        cb_annotation = QComboBox()
        box_select.addWidget(cb_annotation)
        btn_open = QPushButton("Загрузить")
        box_select.addWidget(btn_open)

        box_nav = QHBoxLayout()
        prev_btn = QPushButton("Предыдущее изображение")
        box_nav.addWidget(prev_btn)
        cb_tag = QComboBox()
        box_nav.addWidget(cb_tag)
        next_btn = QPushButton("Следующее изображение")
        box_nav.addWidget(next_btn)

        vbox.addLayout(box_select)
        vbox.addWidget(image_view)
        vbox.addLayout(box_nav)

        window.setLayout(vbox)
        self.setCentralWidget(window)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())




