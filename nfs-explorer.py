import sys
import subprocess
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit, QListWidget

class NFSExplorer(QWidget):
    """
    Page that displays the existing files in the file system as part of the file explorer
    """
    def __init__(self, server_ip, server_mount_point):
        super().__init__()
        self.server_ip = server_ip
        self.server_mount_point = server_mount_point
        self.initUI()
    
    def initUI(self):
        self.file_list = QListWidget()

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh_files)

        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.download_file)

        self.file_label = QLabel('Selected File:')
        self.file_path_label = QLabel('')

        layout = QGridLayout()
        layout.addWidget(self.file_list, 0, 0, 1, 3)
        layout.addWidget(self.refresh_button, 1, 0)
        layout.addWidget(self.download_button, 1, 1)
        layout.addWidget(self.file_label, 2, 0)
        layout.addWidget(self.file_path_label, 2, 1, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle('NFS Explorer')

        self.refresh_files()
        self.show()

    def refresh_files(self):
        self.file_list.clear()

        try:
            files = os.listdir(self.server_mount_point)
            print(files)
            self.file_list.addItems(files)
            print(f'Successfully refreshed files from NFS server {self.server_ip}')
        except OSError as e:
            print(f'Error refreshing files from NFS server {self.server_ip}: {e}')

    def download_file(self):
        file_name = self.file_list.currentItem().text()

        if file_name:
            source_path = os.path.join(self.server_mount_point, file_name)
            target_path, _ = QFileDialog.getSaveFileName(self, 'Save file', file_name)

            if target_path:
                try:
                    shutil.copyfile(source_path, target_path)
                    print(f'Successfully downloaded file {file_name}')
                except IOError as e:
                    print(f'Error downloading file {file_name}: {e}')
        else:
            print('Please select a file')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #ip_input = QLineEdit()
    #mount_point_input = QLineEdit()
    nfsExp = NFSExplorer('10.0.62.165', '/home/sky')
    sys.exit(app.exec_())