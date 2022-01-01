import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt


class startup(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(256, 128)
        #self.centre()
        grid = QGridLayout()

        button1 = QPushButton("Existing Account")
        button1.clicked.connect(self.login)
        button2 = QPushButton("New Account")
        button2.clicked.connect(self.newUser)

        l1 = QLabel(self)
        l1.setText("Temporary")
        l1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(l1, 0, 0, 0, 1)
        grid.addWidget(button1, 1, 0)
        grid.addWidget(button2, 1, 1)

        self.setLayout(grid)


        self.setWindowTitle('Startup')
        self.show()



    def centre(self):
        qr = self.frameGeometry()
        print(qr)
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def login(self, checked):
        print("current")

    def newUser(self):
        print("new")


def main():

    app = QApplication(sys.argv)
    x = startup()
    sys.exit(app.exec())

if __name__ == "__main__":

    main()