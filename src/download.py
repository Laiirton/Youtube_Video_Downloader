from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube


class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            yt = YouTube(self.url)
            stream = yt.streams.get_highest_resolution()
            stream.download()

            # Atualizando a barra de progresso
            total_size = stream.filesize
            bytes_downloaded = 0
            for data in stream.stream_to_buffer():
                bytes_downloaded += len(data)
                progress = int(100 * bytes_downloaded / total_size)
                self.progress_signal.emit(progress)

        except Exception as e:
            print(f"Erro no download: {e}")
