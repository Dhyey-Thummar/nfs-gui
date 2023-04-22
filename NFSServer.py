import sys
import subprocess
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit
from NFSClient import NFSClientGUI


class NFSServerGUI(QWidget):
    """
    NFS Server GUI which displays the options to setup the NFS share and does the setup of nfs that is installing nfs-kernel-server package
    and setting up the nfs share, and also displays the option to start the nfs server, ie giving option to add the ip on which to share which folder with what permisisons and gcing the necessary changes to /etc/exports file and exportfs -a command, etc,
    and also
    the option to stop the nfs server
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
        # server = self.server_combo.currentText()
        server = self.server_ip_edit.text()
        mount_point_server = self.mount_point_edit_server.text()
        mount_point_client = self.mount_point_edit_client.text()
        print(server, mount_point_server, mount_point_client)
        # self.client = NFSClient(server, mount_point_server, mount_point_client)
        # self.client.connect_to_server()
        self.client = NFSClientGUI(server, mount_point_server, mount_point_client)
        self.client.show()
        self.hide()
    
    def browse_files(self):
        file_path = QFileDialog.getOpenFileName(self, 'Select File')
        self.file_path_label.setText(file_path[0])
    
    def upload_file(self):
        file_path = self.file_path_label.text()
        self.client.upload_file(file_path)
    
    def download_file(self):
        file_path = self.file_path_label.text()
        self.client.download_file(file_path)
    
    def closeEvent(self, event):
        self.client.close()
        event.accept()