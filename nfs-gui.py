import sys
import subprocess
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit

class NFSClientGUI(QWidget):
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
        server_ip = self.server_ip_edit.text()
        mount_point_server = self.mount_point_edit_server.text()
        mount_point_client = self.mount_point_edit_client.text()

        if not server_ip or not mount_point_server or not mount_point_client:
            print('Please enter the server IP and mount point server and client')
            return

        try:
            subprocess.check_call(['sudo', 'mount', server_ip,':', mount_point_server, mount_point_client ])
            print(f'Successfully mounted NFS server {server_ip}')
        except subprocess.CalledProcessError as e:
            print(f'Error mounting NFS server {server_ip}: {e}')


    def browse_files(self):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(self, 'Select file')[0]
        self.file_path_label.setText(file_path)

    def upload_file(self):
        file_path = self.file_path_label.text()
        mount_point = '/mnt/nfs'

        if file_path and self.is_mounted(mount_point):
            file_name = os.path.basename(file_path)
            target_path = os.path.join(mount_point, file_name)

            try:
                shutil.copyfile(file_path, target_path)
                print(f'Successfully uploaded file {file_name}')
            except IOError as e:
                print(f'Error uploading file {file_name}: {e}')
        else:
            print('Please select a file and mount an NFS server')

    def is_mounted(self, mount_point):
        with open('/proc/mounts', 'r') as f:
            for line in f:
                if line.startswith('nfs ') and line.split()[1] == mount_point:
                    return True
            return False

    def download_file(self):
        file_name = self.file_list.currentItem().text()
        mount_point = '/mnt/nfs'

        if file_name and self.is_mounted(mount_point):
            source_path = os.path.join(mount_point, file_name)
            target_path, _ = QFileDialog.getSaveFileName(self, 'Save file', file_name)

            if target_path:
                try:
                    shutil.copyfile(source_path, target_path)
                    print(f'Successfully downloaded file {file_name}')
                except IOError as e:
                    print(f'Error downloading file {file_name}: {e}')
        else:
            print('Please select a file and mount an NFS server')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = NFSClientGUI()
    sys.exit(app.exec_())
