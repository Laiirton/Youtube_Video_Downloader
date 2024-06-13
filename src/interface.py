from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QPalette, QFont
from PySide6.QtCore import Qt

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        # Configurando a janela principal
        self.setWindowTitle("YouTube Downloader")
        self.setFixedSize(800, 600)
        
        # Definindo o fundo
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QPixmap("./src/assets/background.jpg"))
        self.setPalette(palette)

        # Criando o título
        self.title = QLabel("YouTube Video Downloader", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Open Sans", 24, QFont.Bold))
        self.title.setStyleSheet("color: #D1D1D1;")

        # Criando o campo de texto
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Copie e cole o URL para baixar")
        self.url_input.setFixedHeight(50)
        self.url_input.setStyleSheet(
            """
            border-radius: 20px; 
            padding: 10px; 
            background-color: #4F4F4F; 
            color: #ffffff; 
            border: 2px solid #5A5A5A;
            font-size: 16px;
            """
        )

        # Criando o botão de download
        self.download_button = QPushButton("BAIXAR", self)
        self.download_button.setFixedHeight(40)
        self.download_button.setStyleSheet(
            """
            background-color: #4B0082; 
            color: #FFFFFF; 
            border-radius: 20px; 
            padding: 10px 20px; 
            font-weight: bold; 
            border: 2px solid #4B0082;
            """
        )

        # Criando layout horizontal para campo de texto e botão
        hbox = QHBoxLayout()
        hbox.addWidget(self.url_input)
        hbox.addWidget(self.download_button)
        
        # Criando layout vertical principal
        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addStretch()
        vbox.addLayout(hbox)
        vbox.addStretch()
        
        # Definindo margens
        vbox.setContentsMargins(50, 50, 50, 200)  # Ajustando margens para melhor centralização
        
        self.setLayout(vbox)

if __name__ == "__main__":
    app = QApplication([])

    window = YouTubeDownloader()
    window.show()

    app.exec()
