import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Configuração da janela principal
app = ctk.CTk()
app.geometry("702x406")
app.title("YouTube Video Downloader")

# Carregar e configurar a imagem de fundo
bg_image = Image.open("./src/assets/background.jpg")
bg_image = ImageTk.PhotoImage(bg_image)
canvas = tk.Canvas(app, width=720, height=406)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Adicionar título diretamente no canvas
canvas.create_text(200, 50, text="YouTube Downloader", font=("Helvetica", 24), fill="white")

# Função de download de vídeo (placeholder)
def download_video():
    print("Downloading video...")

# Adicionar botão de download
button = tk.Button(app, text="Download Video", command=download_video)
button_window = canvas.create_window(550, 310, anchor="center", window=button)

# Executar a aplicação
app.mainloop()