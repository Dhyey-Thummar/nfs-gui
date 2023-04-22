import sys
import subprocess
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit
from NFSClient import NFSClientGUI
from NFSServer import NFSServerGUI


class StartPage(QWidget):
    """
    Start page of the application
    It displays option of selecting how to setup the NFS share as client or server or both.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.server_label = QLabel('NFS Server:')
        self.server_combo = QComboBox()
        self.server_combo.addItem('Client')
        self.server_combo.addItem('Server')

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_to_server)

        layout = QGridLayout()
        layout.addWidget(self.server_label, 0, 0)
        layout.addWidget(self.server_combo, 0, 1)
        layout.addWidget(self.connect_button, 0, 2)

        self.setLayout(layout)
        self.setWindowTitle('NFS Client GUI')
        self.show()

    def connect_to_server(self):
        server = self.server_combo.currentText()
        if server == 'Client':
            self.client = NFSClientGUI()
            self.close()
        elif server == 'Server':
            self.server = NFSServerGUI()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartPage()
    sys.exit(app.exec_())
