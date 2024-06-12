# Download thread related imports
from PySide6.QtCore import QThread, Signal
import yt_dlp
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
        # Função para formatar a velocidade de download em uma string legível
        # Exemplo: "1.23 MB/s"
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        while speed >= 1024 and unit_index < len(units) - 1:
            speed /= 1024
            unit_index += 1
        return f"{speed:.2f} {units[unit_index]}"