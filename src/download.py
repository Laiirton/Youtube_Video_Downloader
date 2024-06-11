from PySide6.QtCore import QThread, Signal
import yt_dlp


class DownloadThread(QThread):
    progress_signal = Signal(int)
    
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

        
    def run(self):
        try:
            ytdl_opts = {}
            if self.parent.download_directory:
                ytdl_opts['outtmpl'] = f'{self.parent.download_directory}/%(title)s.%(ext)s'
                
            with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                file_size = info.get('requested_downloads')[0]['total_bytes']
                
                progress_hooks = [self.update_progress(file_size)]
                ydl.add_progress_hook(progress_hooks)
                
        except Exception as e:
            print(e)