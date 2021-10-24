import sys
from PyQt6.QtWidgets import QApplication, QWidget

class startup(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(1500, 1000)
        self.centre()
        self.setWindowTitle('Startup')
        self.show()

        sys.exit(app.exec())

    def centre(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = QApplication(sys.argv)
x = startup()