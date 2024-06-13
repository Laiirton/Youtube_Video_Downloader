import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Configuração da janela principal
app = ctk.CTk()
app.geometry("800x600")
app.title("YouTube Video Downloader")

# Carregar e configurar a imagem de fundo
bg_image = Image.open("./src/assets/background.jpg")
bg_image = bg_image.resize((800, 600), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(app, width=800, height=600, highlightthickness=0)  # Remover borda do canvas
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# Adicionar título diretamente no canvas com fundo e borda
title_text = "YouTube Downloader"
font = ("Roboto", 40, 'bold')
title_bg_color = "black"
title_text_color = "white"
title_border_color = "white"
title_border_width = 3

title_id = canvas.create_text(400, 50, text=title_text, font=font, fill=title_text_color)

# Adicionar fundo ao texto
x1, y1, x2, y2 = canvas.bbox(title_id)
padding = 10
x1 -= padding
y1 -= padding
x2 += padding
y2 += padding
canvas.create_rectangle(x1, y1, x2, y2, fill=title_bg_color, outline=title_border_color, width=title_border_width)
canvas.tag_raise(title_id)

# Função de download de vídeo (placeholder)
def download_video():
    print("Downloading video...")

# Frame para URL e botão de download
url_frame = ctk.CTkFrame(app, width=400, height=40, corner_radius=20)
url_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Campo de texto para URL
url_entry = ctk.CTkEntry(url_frame, width=300, height=40, corner_radius=20, placeholder_text="Enter video URL")
url_entry.pack(side=tk.LEFT, padx=10, pady=5)

# Botão de download dentro do campo de URL
download_button = ctk.CTkButton(url_frame, text="Download", width=80, height=40, corner_radius=20, command=download_video)
download_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Executar a aplicação
app.mainloop()
