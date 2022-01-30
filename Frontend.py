import sys
import Backend as be
import time
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt

loggedIn = False

class signUp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sign Up')

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

        global w

        if be.newAcc(str(self.lineEdits['password']), str(self.lineEdits['key']), str(self.lineEdits['secret']), str(self.lineEdits['walletName'])) == True:
            self.worked.setText('Successful')
            w.layout.setCurrentIndex(1)
            time.sleep(3)
            self.close()
        else:
            self.worked.setText('Unsuccessful')



class login(QWidget):

    def __init__(self):
        super(login, self).__init__()

        self.setWindowTitle('Login')

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

        global w

        if be.passCheck(str(self.password)) == True:
            self.worked.setText('Successful')
            w.layout.setCurrentIndex(1)
            time.sleep(3)
            self.close()
        else:
            self.worked.setText('Unsuccessful')



class mainWindow(QMainWindow):

    def __init__(self):
        global loggedIn

        super().__init__()

        self.setWindowTitle('Sigmund')

        self.resize(1024, 512)
        self.centre()
        self.layout = QStackedLayout()

        self.start = startWindow()
        self.work = workWindow()
        self.layout.addWidget(self.start)
        self.layout.addWidget(self.work)

        self.layout.setCurrentIndex(0)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)



    def centre(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class startWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.l = None
        self.n = None
        self.go = True

        self.button1 = QPushButton("Existing Account")
        self.button1.clicked.connect(self.login)
        self.button2 = QPushButton("New Account")
        self.button2.clicked.connect(self.newAcc)


        outLayout = QVBoxLayout()
        layout = QHBoxLayout()

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        outLayout.addLayout(layout)


        self.setLayout(outLayout)


    def login(self, checked):
        if self.l is None:
            self.l = login()
            self.l.show()

        else:
            self.l.close()  # Close window.
            self.l = None

    def newAcc(self, checked):

        accExists = be.initCheck()

        if self.n is None:
            self.n = signUp()
            self.n.show()

        else:
            self.n.close()  # Close window.
            self.n = None



class workWindow(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        tabWidget = QTabWidget()
        tabWidget.setMovable(True)

        for i in range(0,5):
            tabWidget.addTab(walletTab(str(i)), str(i))

        layout.addWidget(tabWidget)
        self.setLayout(layout)


class walletTab(QWidget):

    def __init__(self, name):
        super().__init__()

        layout = QVBoxLayout()
        layout2 = LayToTab(name)

        self.chart = Label(f'chart{name}')
        splitter1 = QSplitter(Qt.Orientation.Vertical)
        splitter1.addWidget(layout2)
        splitter1.addWidget(self.chart)
        layout.addWidget(splitter1)
        self.setLayout(layout)


class LayToTab(QWidget):

    def __init__(self, name):
        super().__init__()

        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()

        layout3.addWidget(Label(f'start/stop{name}'))
        layout3.addWidget(Label(f'{name} current value'))
        layout2.addLayout(layout3)

        layout2.addWidget(Label(f'{name} trading history'))
        layout2.addWidget(Label(f'{name} current positions'))

        self.setLayout(layout2)


def Label(content):

    out = QLabel(content)
    out.setStyleSheet("border: 1px solid black;")
    return out

app = QApplication(sys.argv)
w = mainWindow()

def main():

    global w, app

    w.show()
    app.exec()

if __name__ == "__main__":

    main()