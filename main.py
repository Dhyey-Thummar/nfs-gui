from StartPage import StartPage
from Client import NFSClientGUI
from Server import NFSServerGUI
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartPage()
    sys.exit(app.exec_())