# Download thread related imports
from PySide6.QtCore import QThread, Signal
import yt_dlp

class DownloadThread(QThread):
    progress_signal = Signal(int)

    def __init__(self, url, download_directory, parent=None):
        super().__init__(parent)
        self.url = url
        self.download_directory = download_directory

    def run(self):
        try:
            ytdl_opts = {}
            if self.download_directory:
                ytdl_opts['outtmpl'] = f'{self.download_directory}/%(title)s.%(ext)s'
                
            with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                file_size = info.get('requested_downloads')[0]['total_bytes']

                def update_progress(d):
                    if d['status'] == 'downloading':
                        percent = d['downloaded_bytes'] / file_size * 100
                        self.progress_signal.emit(int(percent))

                ydl.add_progress_hook(update_progress)

        except Exception as e:
            print(e)
