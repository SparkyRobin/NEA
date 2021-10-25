import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import inspect

class startup(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(1000, 1000)
        self.centre()
        self.vlay = QVBoxLayout(self)
        #self.vlay.addItem(QSpacerItem(0, 0))
        #self.vlay.addStretch(1)
        self.button("Sam", y=300)
        self.button("Parker")
        #self.vlay.addStretch(1)
        #self.vlay.addItem(QSpacerItem(0, 0))
        self.hlay = QHBoxLayout(self)
        self.hlay.addStretch(1)
        self.hlay.addLayout(self.vlay)
        self.setWindowTitle('Startup')
        self.centre()
        self.show()

    def button(self, name, x=0, y=0):
        self.btn = QPushButton(name, self)
        self.btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.vlay.addWidget(self.btn)



    def centre(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

app = QApplication(sys.argv)
x = startup()
sys.exit(app.exec())