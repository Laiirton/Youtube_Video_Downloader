# Main window related imports
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QFileDialog
from PySide6.QtCore import Slot
from download import DownloadThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.download_directory = None

        # Layout da interface
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Elementos da interface(url,button,progress bar)
        self.url_input = QLineEdit()
        self.download_button = QPushButton("Download")
        self.progress_bar = QProgressBar()
        self.directory_button = QPushButton("Select Directory")

        # Elementos Layout
        layout.addWidget(QLabel("Link Url:"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.directory_button)

        # Conectando os botões
        self.directory_button.clicked.connect(self.select_directory)
        self.download_button.clicked.connect(self.start_download)

    @Slot()
    def select_directory(self):
        self.download_directory = QFileDialog.getExistingDirectory(self, "Select download directory")

    @Slot()
    def start_download(self):
        url = self.url_input.text()
        self.thread = DownloadThread(url, self.download_directory)
        self.thread.progress_signal.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
