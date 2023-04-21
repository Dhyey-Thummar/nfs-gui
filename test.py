import sys
import subprocess
import shutil
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog, QGridLayout, QLineEdit, QTreeWidget, QTreeWidgetItem

class NFSExplorer(QWidget):
    """
    Page that displays the existing files in the file system as part of the file explorer
    """
    def __init__(self, path):
        super().__init__()
        self.current_path = path
        self.initUI()

    def initUI(self):
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['Name', 'Type', 'Size'])
        self.tree_widget.itemDoubleClicked.connect(self.handle_tree_item_double_clicked)
        
        layout = QGridLayout()
        layout.addWidget(self.tree_widget, 0, 0)

        self.setLayout(layout)
        self.setWindowTitle('NFS Explorer')
        self.show()

        self.update_directory(self.current_path)

    def update_directory(self, path):
        self.current_path = path
        self.tree_widget.clear()

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            item_size = os.path.getsize(item_path)
            item_type = 'Directory' if os.path.isdir(item_path) else 'File'
            item_size_str = f'{item_size} bytes'

            tree_item = QTreeWidgetItem([item, item_type, item_size_str])
            if os.path.isdir(item_path):
                tree_item.addChild(QTreeWidgetItem(['Loading...', '', '']))
            self.tree_widget.addTopLevelItem(tree_item)

    def handle_tree_item_double_clicked(self, item, column):
        if item.childCount() > 0:
            # Directory was double-clicked
            self.update_directory(os.path.join(self.current_path, item.text(0)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = NFSExplorer('/home/sky')
    sys.exit(app.exec_())
