import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QFileDialog
)
import launch
from pathlib import Path

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Scarlett\'s Youtube Downloader')

        # Create Widgets
        # First Row
        self.row_1_label_1 = QLabel('Please Enter URL or browse for Error file:')
        self.row_1_line_edit_1=QLineEdit()

        self.row_1_button_1=QPushButton('Browse')
        # Second Row


        # Actions
        #line_edit.textChanged.connect(label.setText)
        self.row_1_button_1.clicked.connect(self.row_1_button_1_clicked)

        # place the widgets
        # Create layout
        layout = QGridLayout()
        # First Row
        frc=[20,35,10]
        layout.setColumnMinimumWidth(0, 30)
        layout.setRowMinimumHeight(0, 10)
        layout.setColumnStretch(0,50)
        layout.setRowStretch(0,50)
        layout.addWidget(self.row_1_label_1, 0,0,1, frc[0])
        layout.addWidget(self.row_1_line_edit_1, 0,frc[0],1,frc[1])
        layout.addWidget(self.row_1_button_1, 0,frc[0]+frc[1],1,frc[2])

        self.setLayout(layout)

        # show the window
        self.show()

    def row_1_button_1_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select a File", filter="*.csv")
        #dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        if filename:
            path = Path(filename)
            self.row_1_line_edit_1.setText(str(path))

            wa