

import sys
import subprocess
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit

class NFSClientGUI(QWidget):
    """
    NFS Client GUI, which will display an option to connect to a server ip and mount files as nfs share, and after clicking on the 
    connect button, it will display the files in the mounted directory, and as well as the option to upload and download files.
    """

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.server_label = QLabel('NFS Server:')
        self.server_ip_label = QLabel('Server IP:')
        self.server_ip_edit = QLineEdit()

        self.mount_point_label_server = QLabel('Server Mount Point:')
        self.mount_point_edit_server = QLineEdit()

        self.mount_point_label_client = QLabel('Client Mount Point:')
        self.mount_point_edit_client = QLineEdit()

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_to_server)

        self.browse_button = QPushButton('Browse...')
        self.browse_button.clicked.connect(self.browse_files)

        self.upload_button = QPushButton('Upload')
        self.upload_button.clicked.connect(self.upload_file)

        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.download_file)

        self.file_label = QLabel('Selected File:')
        self.file_path_label = QLabel('')

        layout = QGridLayout()
        layout.addWidget(self.server_label, 0, 0)
        layout.addWidget(self.server_ip_label, 1, 0)
        layout.addWidget(self.server_ip_edit, 1, 1)
        layout.addWidget(self.mount_point_label_server, 2, 0)
        layout.addWidget(self.mount_point_edit_server, 2, 1)
        layout.addWidget(self.mount_point_label_client, 3, 0)
        layout.addWidget(self.mount_point_edit_client, 3, 1)
        layout.addWidget(self.connect_button, 3, 2)
        layout.addWidget(self.browse_button, 4, 0)
        layout.addWidget(self.upload_button, 4, 1)
        layout.addWidget(self.download_button, 4, 2)
        layout.addWidget(self.file_label, 5, 0)
        layout.addWidget(self.file_path_label, 5, 1, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle('NFS Client GUI')
        self.show()

    def connect_to_server(self):
        server = self.server_ip_edit.text()
        mount_point_server = self.mount_point_edit_server.text()
        mount_point_client = self.mount_point_edit_client.text()
        subprocess.call(['sudo', 'mount', '-t', 'nfs', server + ':' + mount_point_server, mount_point_client])

    def browse_files(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.file_path_label.setText(directory)
    
    def upload_file(self):
        source = self.file_path_label.text()
        destination = self.mount_point_edit_client.text()
        shutil.copy(source, destination)
    
    def download_file(self):
        source = self.mount_point_edit_client.text()
        destination = self.file_path_label.text()
        shutil.copy(source, destination)
    
