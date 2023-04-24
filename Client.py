

import sys
import subprocess
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit
from PyQt5 import QtGui, QtCore
from Explorer import NFSExplorer


class NFSClientGUI(QWidget):
    """
    NFS Client GUI, which will display an option to connect to a server ip and mount files as nfs share, and after clicking on the 
    connect button, it will display the files in the mounted directory, and as well as the option to upload and download files.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.server_label = QLabel('NFS Client Setup')
        self.server_ip_label = QLabel('Server IP:')
        self.server_ip_edit = QLineEdit()

        self.mount_point_label_server = QLabel('Server Mount Point:')
        self.mount_point_edit_server = QLineEdit()

        self.mount_point_label_client = QLabel('Client Mount Point:')
        self.mount_point_edit_client = QLineEdit()

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_to_server)

        self.check_mount_button = QPushButton('Check Mount')
        self.check_mount_button.clicked.connect(self.check_mount_fn)
        self.mount_label = QLabel('Mount Status:')
        self.mount_status = QLabel('Not Mounted')

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.back_button_clicked)

        layout = QGridLayout()
        layout.addWidget(self.server_label, 0, 1,
                         alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.server_ip_label, 1, 0)
        layout.addWidget(self.server_ip_edit, 1, 1)
        layout.addWidget(self.mount_point_label_server, 2, 0)
        layout.addWidget(self.mount_point_edit_server, 2, 1)
        layout.addWidget(self.mount_point_label_client, 3, 0)
        layout.addWidget(self.mount_point_edit_client, 3, 1)

        layout.addWidget(self.check_mount_button, 4, 0)
        layout.addWidget(self.mount_label, 4, 1)
        layout.addWidget(self.mount_status, 4, 2)
        layout.addWidget(self.back_button, 5, 0)
        layout.addWidget(self.connect_button, 5, 2)

        self.setLayout(layout)
        self.setWindowTitle('NFS Client')
        self.show()

    def check_mount(self, mount_point_client):
        if os.path.ismount(mount_point_client):
            print('NFS share mounted')
            return True
        else:
            print('NFS share not mounted')
        return False

    def check_mount_fn(self):
        mount_point_client = self.mount_point_edit_client.text()
        if self.check_mount(mount_point_client):
            self.mount_status.setText('Mounted')
        else:
            self.mount_status.setText('Not Mounted')

    def connect_to_server(self):
        # server = self.server_combo.currentText()
        server_ip = self.server_ip_edit.text()
        mount_point_server = self.mount_point_edit_server.text()
        mount_point_client = self.mount_point_edit_client.text()

        if not server_ip or not mount_point_server or not mount_point_client:
            print('Please enter the server IP and mount point server and client')
            return

        # if self.check_mount(mount_point_client):
        #     print('NFS share already mounted')
        #     self.explorer = NFSExplorer(server_ip, mount_point_client)
        #     self.close()

        self.explorer = NFSExplorer(server_ip, mount_point_client)
        self.close()

        try:
            subprocess.call(['sudo', 'mount', '-t', 'nfs', server_ip + ':' + mount_point_server, mount_point_client])
            print(f'Successfully mounted NFS server {server_ip}')
            self.explorer = NFSExplorer(server_ip, mount_point_client)
            self.close()
        except Exception as e:
            print(f'Error mounting NFS server {server_ip}: {e}')
        finally:
            print('connect_to_server() finished')

    def back_button_clicked(self):
        from StartPage import StartPage
        self.startpage = StartPage()
        self.close()
