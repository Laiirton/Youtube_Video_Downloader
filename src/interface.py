from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QFileDialog, QMessageBox, QHBoxLayout
from PySide6.QtCore import Slot, Qt, QThread, Signal
from PySide6.QtGui import QScreen, QGuiApplication
import qtawesome as qta
import yt_dlp
import re
import time

class DownloadThread(QThread):
    progress_signal = Signal(int)
    speed_signal = Signal(str)

    def __init__(self, url, download_directory, parent=None):
        super().__init__(parent)
        self.url = url
        self.download_directory = download_directory
        self.last_downloaded_size = 0
        self.last_time = time.time()

    def run(self):
        try:
            ytdl_opts = {
                'progress_hooks': [self.update_progress],
                'outtmpl': f'{self.download_directory}/%(title)s.%(ext)s' if self.download_directory else '%(title)s.%(ext)s'
            }

            with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                ydl.download([self.url])

        except Exception as e:
            print(e)

    def update_progress(self, d):
        if d['status'] == 'downloading':
            total_size = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_size = d.get('downloaded_bytes', 0)
            if total_size:
                percent = int(downloaded_size / total_size * 100)
                self.progress_signal.emit(percent)

                # Calcular a velocidade de download
                current_time = time.time()
                downloaded_bytes = downloaded_size - self.last_downloaded_size
                elapsed_time = current_time - self.last_time
                if elapsed_time > 0:
                    speed = downloaded_bytes / elapsed_time
                    speed_str = self.format_speed(speed)
                    self.speed_signal.emit(speed_str)

                self.last_downloaded_size = downloaded_size
                self.last_time = current_time

    def format_speed(self, speed):
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        while speed >= 1024 and unit_index < len(units) - 1:
            speed /= 1024
            unit_index += 1
        return f"{speed:.2f} {units[unit_index]}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 600, 400)
        self.download_directory = None
        self.start_time = None

        self.center_window()

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL...")
        self.download_button = QPushButton(qta.icon('fa.download', color='white'), " Download")
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_label = QLabel("0%")
        self.directory_button = QPushButton(qta.icon('fa.folder-open', color='white'), " Select Directory")

        layout.addWidget(QLabel("Link URL:", alignment=Qt.AlignCenter))
        layout.addWidget(self.url_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.directory_button)
        buttons_layout.addWidget(self.download_button)
        layout.addLayout(buttons_layout)

        layout.addWidget(self.progress_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.directory_button.clicked.connect(self.select_directory)
        self.download_button.clicked.connect(self.start_download)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                font-size: 16px;
                color: #ecf0f1;
            }
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QPushButton {
                font-size: 16px;
                background-color: #e74c3c;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QProgressBar {
                height: 30px;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                background-color: #34495e;
            }
            QProgressBar::chunk {
                background-color: #e74c3c;
                border-radius: 5px;
            }
        """)

    def center_window(self):
        screen_geometry = QScreen.availableGeometry(QGuiApplication.primaryScreen())
        screen_center = screen_geometry.center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    @Slot()
    def select_directory(self):
        self.download_directory = QFileDialog.getExistingDirectory(self, "Select download directory")

    @Slot()
    def start_download(self):
        self.start_time = time.time()
        url = self.url_input.text()
        if not self.is_valid_url(url):
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid URL.")
            return

        if not self.download_directory:
            QMessageBox.warning(self, "No Directory Selected", "Please select a download directory.")
            return

        self.thread = DownloadThread(url, self.download_directory)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.speed_signal.connect(self.update_speed)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()

    @Slot(str)
    def update_speed(self, speed):
        self.progress_label.setText(f"{self.thread.percent}% - Speed: {speed}")

    def download_finished(self):
        QMessageBox.information(self, "Download Complete", "The video has been downloaded successfully.")
        self.thread.deleteLater()

    def is_valid_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.thread.percent = value