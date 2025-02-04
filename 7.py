import os
import sys


import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.map_ll = [37.530887, 55.703118]
        self.zoom = 10
        self.delta = 0.01
        self.image = QLabel(self)
        self.getImage()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll_spn = f'll={self.map_ll[0]},{self.map_ll[1]}&z={self.zoom}'

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        self.setFocus()
        if key == Qt.Key.Key_PageDown and self.zoom > 0:
            self.zoom += 1
        if key == Qt.Key.Key_PageUp and self.zoom < 18:
            self.zoom -= 1
        if key == Qt.Key.Key_Left:
                self.map_ll[0] -= self.delta
        if key == Qt.Key.Key_Right:
            self.map_ll[0] += self.delta
        if key == Qt.Key.Key_Up:
                self.map_ll[1] -= self.delta
        if key == Qt.Key.Key_Down:
                self.map_ll[1] += self.delta
        self.getImage()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())