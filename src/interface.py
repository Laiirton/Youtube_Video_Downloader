import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Configuração da janela principal
app = ctk.CTk()
app.geometry("800x600")
app.title("YouTube Video Downloader")
app.resizable(False, False)

# Carregar e configurar a imagem de fundo
bg_image = Image.open("./src/assets/background.jpg")
bg_image = bg_image.resize((800, 600), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(app, width=800, height=600, highlightthickness=0)  # Remover borda do canvas
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Cria um contorno suavizado para o texto
offsets = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
for x, y in offsets: 
    # Adicionar título diretamente no canvas
    canvas.create_text(200 + x, 50 + y, text="YouTube Downloader", font=("Helvetica", 24,), fill="white", anchor="center")

# Função de download de vídeo (placeholder)
def download_video():
    print("Downloading video...")

# Adicionar botão de download
button = ctk.CTkButton(app, text="Download Video", command=download_video)
button_window = canvas.create_window(400, 310, anchor="center", window=button)

# Executar a aplicação
app.mainloop()
