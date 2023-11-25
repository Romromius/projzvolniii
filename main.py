import sqlite3
import sys
import winsound
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (QApplication, QListWidget, QLineEdit, QComboBox, QMainWindow, QLabel)


class Library(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1, 1)
        self.setWindowTitle('Библиотека')
        self.setFixedSize(420, 485)  # Важно!
        self.dat = sqlite3.connect('coffee.sqlite')
        self.cur = self.dat.cursor()

        # ~ Виджеты ~

        self.results = QListWidget(self)
        self.results.resize(200, 465)
        self.results.move(10, 10)


        self.info = QLabel(self)
        self.info.resize(180, 465)
        self.info.move(220, 10)
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setFont(QFont('Times New Roman', 11))

        # ~ Коннекторы ~

        self.results.currentItemChanged.connect(self.fetch)
        self.update_coffe()
        winsound.Beep(3000, 50)
        winsound.Beep(4000, 50)

    def bep(self):
        winsound.Beep(1000, 100)

    def update_coffe(self):
        raw = self.cur.execute('''SELECT sort FROM menu''').fetchall()
        self.results.addItems([i[0] for i in raw])

    def fetch(self):
        threading.Thread(target=self.bep).start()

        return
        raw = self.cur.execute('''SELECT * FROM coffee''')
        self.info.setText(raw)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Library()
    ex.show()
    sys.exit(app.exec())
