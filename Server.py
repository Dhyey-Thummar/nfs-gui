import sys
import subprocess
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit, QErrorMessage
from Client import NFSClientGUI
from PyQt5 import QtGui, QtCore


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
            self.setWindowIcon(QtGui.QIcon('logo.png'))
            self.server_label = QLabel('NFS Server Setup')
            self.server_label.setStyleSheet("font: bold 20px")
            self.server_label.setAlignment(QtCore.Qt.AlignCenter)

            self.client_ip_to_share_label = QLabel('Enter the IP of the client to share the folder with: ')
            self.client_ip_to_share_edit = QLineEdit()

            self.folder_to_share_label = QLabel('Enter the folder to share: ')
            self.folder_to_share_edit = QLineEdit()

            self.permissions_label = QLabel('Enter the permissions: ')
            self.permissions_edit = QLineEdit()

            self.add_button = QPushButton('Add')
            self.add_button.clicked.connect(self.add_button_clicked)

            self.check_server_status_button = QPushButton('Check Server Status')
            self.check_server_status_button.clicked.connect(self.check_server_status_button_clicked)
            self.server_status_label = QLabel('Server Status:')
            self.server_status = QLabel('Not Running')
            self.server_status.setStyleSheet("color: red")


            self.start_server_button = QPushButton('Start Server')
            self.start_server_button.clicked.connect(self.start_server_button_clicked)

            self.stop_server_button = QPushButton('Stop Server')
            self.stop_server_button.clicked.connect(self.stop_server_button_clicked)

            self.back_button = QPushButton('Back')
            self.back_button.clicked.connect(self.back_button_clicked)

            self.show_exported_folders_button = QPushButton('Show Exported Folders')
            self.show_exported_folders_button.clicked.connect(self.show_exported_folders_button_clicked)


            layout = QGridLayout()
            layout.addWidget(self.server_label, 0, 1, alignment=QtCore.Qt.AlignCenter)
            layout.addWidget(self.client_ip_to_share_label, 1, 0)
            layout.addWidget(self.client_ip_to_share_edit, 1, 1)
            layout.addWidget(self.folder_to_share_label, 2, 0)
            layout.addWidget(self.folder_to_share_edit, 2, 1)
            layout.addWidget(self.permissions_label, 3, 0)
            layout.addWidget(self.permissions_edit, 3, 1)
            layout.addWidget(self.add_button, 4, 0)
            layout.addWidget(self.check_server_status_button, 1, 2)
            layout.addWidget(self.server_status_label, 2, 2)
            layout.addWidget(self.server_status, 2, 3)
            layout.addWidget(self.start_server_button, 4, 1)
            layout.addWidget(self.stop_server_button, 4, 2)
            layout.addWidget(self.show_exported_folders_button, 4, 3)
            layout.addWidget(self.back_button, 5, 0)

            self.setLayout(layout)
            self.setWindowTitle('NFS Server Setup')
            self.show()

    def add_button_clicked(self):
        client_ip = self.client_ip_to_share_edit.text()
        folder_to_share = self.folder_to_share_edit.text()
        permissions = self.permissions_edit.text()
        if client_ip == '' or folder_to_share == '' or permissions == '':
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Please enter all the fields to continue.')
            error_dialog.setWindowIcon(QtGui.QIcon('logo.png'))
            error_dialog.setWindowTitle('Error')
            error_dialog.exec_()
        else:
            with open('/etc/exports', 'a') as f:
                f.write(folder_to_share + ' ' + client_ip + '(' + permissions + ')' + '\n')
            self.client_ip_to_share_edit.clear()
            self.folder_to_share_edit.clear()
            self.permissions_edit.clear()

    def start_server_button_clicked(self):
        subprocess.call(['exportfs', '-a'])
        subprocess.call(['systemctl', 'restart', 'nfs-kernel-server'])

    def stop_server_button_clicked(self):
        subprocess.call(['systemctl', 'stop', 'nfs-kernel-server'])
    
    def back_button_clicked(self):
        self.close()
        from StartPage import StartPage
        self.startpage = StartPage()
        self.close()

    def check_server_status_button_clicked(self):
        status = subprocess.check_output(['systemctl', 'status', 'nfs-kernel-server'])
        if 'Active: active (running)' in str(status):
            self.server_status.setText('Running')
            self.server_status.setStyleSheet("color: green")
        else:
            self.server_status.setText('Not Running')
            self.server_status.setStyleSheet("color: red")
    
    def closeEvent(self, event):
        self.close()
        from StartPage import StartPage
        self.startpage = StartPage()
        self.close()

    def show_exported_folders_button_clicked(self):
        os = subprocess.check_output(['uname', '-o'])
        if 'GNU/Linux' in str(os):
            result = subprocess.call(['cat', '/etc/exports'])
        else:
            subprocess.call(['type', 'nfsd'])
            subprocess.call(['cat', '/etc/exports'])
            subprocess.call(['showmount', '-e', 'localhost'])
            subprocess.call(['exportfs', '-v'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    nfs_server_setup = NFSServerGUI()
    sys.exit(app.exec_())