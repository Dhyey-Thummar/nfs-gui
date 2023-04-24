import sys
import subprocess
import shutil
import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit, QRadioButton, QErrorMessage


class StartPage(QWidget):
    """
    Start page of the application
    It displays option of selecting how to setup the NFS share as client or server or both.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.server_label = QLabel('Select how to setup this machine as: ')
        self.server_combo = QRadioButton('Server')
        self.client_combo = QRadioButton('Client')
        self.server_combo.setChecked(False)

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.select_setup)

        layout = QGridLayout()
        layout.addWidget(self.server_label, 0, 0)
        layout.addWidget(self.server_combo, 1, 0,
                         alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.client_combo, 2, 0,
                         alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.connect_button, 3, 1)

        self.setLayout(layout)
        self.setWindowTitle('NFS Setup')
        self.show()

    def select_setup(self):
        if self.server_combo.isChecked():
            from Server import NFSServerGUI
            self.server = NFSServerGUI()
            self.close()
        elif self.client_combo.isChecked():
            from Client import NFSClientGUI
            self.client = NFSClientGUI()
            self.close()
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Please select an option to continue.')
            error_dialog.setWindowIcon(QtGui.QIcon('logo.png'))
            error_dialog.setWindowTitle('Error')
            error_dialog.exec_()
