import sys
import Backend as be
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt


class signUp(QWidget):

    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        layoutPass = QHBoxLayout()

        self.lineEdits = {}

        self.lineEdits['walletName'] = QLineEdit()
        self.lineEdits['key'] = QLineEdit()
        self.lineEdits['secret'] = QLineEdit()
        self.lineEdits['password'] = QLineEdit()
        self.lineEdits['password'].setEchoMode(QLineEdit.EchoMode.Password)

        self.radiobutton = QRadioButton('Hidden')
        self.radiobutton.toggled.connect(self.hidden)

        layoutPass.addWidget(self.lineEdits['password'])
        layoutPass.addWidget(self.radiobutton)

        self.worked = QLabel('')

        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.attempt)

        layout.addRow(QLabel('wallet name'), self.lineEdits['walletName'])
        layout.addRow(QLabel('key'), self.lineEdits['key'])
        layout.addRow(QLabel('secret'), self.lineEdits['secret'])
        layout.addRow(QLabel('password'), layoutPass)
        layout.addRow(self.submit, self.worked)

        self.setLayout(layout)

    def hidden(self):

        if self.radiobutton.isChecked():
            self.lineEdits['password'].setEchoMode((QLineEdit.EchoMode.Normal))
        else:
            self.lineEdits['password'].setEchoMode((QLineEdit.EchoMode.Password))

    def attempt(self):

        if be.newAcc(str(self.lineEdits['password']), str(self.lineEdits['key']), str(self.lineEdits['secret']), str(self.lineEdits['walletName'])) == True:
            self.worked.setText('Successful')
        else:
            self.worked.setText('Unsuccessful')



class login(QWidget):

    def __init__(self):
        super(login, self).__init__()

        layout = QFormLayout()
        layoutPass = QHBoxLayout()

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.radiobutton = QRadioButton('Hidden')
        self.radiobutton.toggled.connect(self.hidden)

        layoutPass.addWidget(self.password)
        layoutPass.addWidget(self.radiobutton)

        self.worked = QLabel('')

        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.attempt)

        layout.addRow(QLabel('password'), layoutPass)
        layout.addRow(self.submit, self.worked)

        self.setLayout(layout)

    def hidden(self):

        if self.radiobutton.isChecked():
            self.password.setEchoMode((QLineEdit.EchoMode.Normal))
        else:
            self.password.setEchoMode((QLineEdit.EchoMode.Password))

    def attempt(self):

        if be.passCheck(str(self.password)) == True:
            self.worked.setText('Successful')
        else:
            self.worked.setText('Unsuccessful')



class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.l = None
        self.n = None

        self.resize(1024, 512)
        self.centre()


        self.button1 = QPushButton("Existing Account")
        self.button1.clicked.connect(self.login)
        self.button2 = QPushButton("New Account")
        self.button2.clicked.connect(self.newAcc)

        outLayout = QVBoxLayout()
        layout = QHBoxLayout()

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        outLayout.addLayout(layout)

        widget = QWidget()
        widget.setLayout(outLayout)
        self.setCentralWidget(widget)

    def login(self, checked):
        if self.l is None:
            self.l = login()
            self.l.show()

        else:
            self.l.close()  # Close window.
            self.l = None

    def newAcc(self, checked):

        # check if already an account before completing

        if self.n is None:
            self.n = signUp()
            self.n.show()

        else:
            self.n.close()  # Close window.
            self.n = None

    def centre(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():

    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    app.exec()

if __name__ == "__main__":

    main()