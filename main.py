import sqlite3
import sys
import winsound

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QListWidget, QMainWindow, QLabel)


class Library(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1, 1)
        self.setWindowTitle('Библиотека')
        self.setFixedSize(520, 485)  # Важно!
        self.dat = sqlite3.connect('coffee.sqlite')
        self.cur = self.dat.cursor()

        # ~ Виджеты ~

        self.results = QListWidget(self)
        self.results.resize(200, 465)
        self.results.move(10, 10)


        self.info = QLabel(self)
        self.info.resize(280, 465)
        self.info.move(220, 10)
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setFont(QFont('Times New Roman', 11))

        # ~ Коннекторы ~

        self.results.currentItemChanged.connect(self.fetch)
        winsound.Beep(3000, 50)
        winsound.Beep(4000, 50)
        self.update_coffe()

    def bep(self):
        winsound.Beep(1000, 100)

    def evil_bep(self):
        winsound.Beep(800, 50)
        winsound.Beep(800, 50)

    def update_coffe(self):
        raw = self.cur.execute('''SELECT sort FROM menu''').fetchall()
        self.results.addItems([i[0] for i in raw])

    def fetch(self):
        self.bep()
        raw = self.cur.execute(f'''SELECT
    sort, roasting, bean, flavor, price, mass
FROM
    menu
INNER JOIN roasting ON
    roasting.id = menu.roasting_id
INNER JOIN flavors ON
    flavors.id = menu.flavor_id
WHERE
    menu.sort = ?''',
                               (self.results.currentItem().text(), )).fetchone()
        raw = [i for i in raw]
        if raw[2]:
            raw[2] = 'В зернах'
        else:
            raw[2] = 'Молотый'
        self.info.setText(f'''{raw.pop(0)}
Обжарка: {raw.pop(0)}
{raw.pop(0)}
{raw.pop(0)}
Цена: {raw.pop(0)}$
Вес: {raw.pop(0)}г.''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Library()
    ex.show()
    sys.exit(app.exec())
