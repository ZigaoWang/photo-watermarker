import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def print_logo():
    logo = r"""
   ___  __        __         _      __     __                         __          
  / _ \/ /  ___  / /____    | | /| / /__ _/ /____ ______ _  ___ _____/ /_____ ____
 / ___/ _ \/ _ \/ __/ _ \   | |/ |/ / _ `/ __/ -_) __/  ' \/ _ `/ __/  '_/ -_) __/
/_/  /_//_/\___/\__/\___/   |__/|__/\_,_/\__/\__/_/ /_/_/_/\_,_/_/ /_/\_\\__/_/   
    """
    print("--------------------------------------------------")
    print(logo)
    print("Photo Watermarker")
    print("Made with 💜 by Zigao Wang.")
    print("This project is licensed under MIT License.")
    print("GitHub Repo: https://github.com/ZigaoWang/photo-watermarker/")
    print("--------------------------------------------------")

def add_image_watermark(image, watermark, position, size):
    image = image.convert("RGBA")
    watermark = watermark.convert("RGBA")

    # Resize the watermark according to the specified size
    watermark = watermark.resize((int(watermark.width * size / 100), int(watermark.height * size / 100)), Image.LANCZOS)

    if position == 'top-left':
        pos = (10, 10)
    elif position == 'top-right':
        pos = (image.width - watermark.width - 10, 10)
    elif position == 'bottom-left':
        pos = (10, image.height - watermark.height - 10)
    elif position == 'bottom-right':
        pos = (image.width - watermark.width - 10, image.height - watermark.height - 10)
    else:
        pos = ((image.width - watermark.width) // 2, (image.height - watermark.height) // 2)

    transparent = Image.new('RGBA', (image.width, image.height), (0, 0, 0, 0))
    transparent.paste(image, (0, 0))
    transparent.paste(watermark, pos, mask=watermark)

    return Image.alpha_composite(image, transparent).convert("RGB")

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        global img
        img = Image.open(file_path)
        preview_image(img)

def open_watermark():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        global watermark
        watermark = Image.open(file_path)
        preview_watermark()

def preview_image(image):
    preview = image.copy()
    preview.thumbnail((800, 800))
    photo = ImageTk.PhotoImage(preview)
    img_label.config(image=photo)
    img_label.image = photo

def preview_watermark():
    if img and watermark:
        watermarked = add_image_watermark(img, watermark, position.get(), size.get())
        preview_image(watermarked)

def save_image():
    if img and watermark:
        watermarked = add_image_watermark(img, watermark, position.get(), size.get())
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if save_path:
            watermarked.save(save_path)
            messagebox.showinfo("Success", "Image saved successfully!")

def update_preview(*args):
    preview_watermark()

img = None
watermark = None

root = tk.Tk()
root.title("Photo Watermarker")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_open_image = tk.Button(frame, text="Open Image", command=open_image)
btn_open_image.grid(row=0, column=0, padx=5, pady=5)

btn_open_watermark = tk.Button(frame, text="Open Watermark", command=open_watermark)
btn_open_watermark.grid(row=0, column=1, padx=5, pady=5)

position = tk.StringVar(value="bottom-right")
positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
for i, pos in enumerate(positions):
    tk.Radiobutton(frame, text=pos.replace("-", " ").title(), variable=position, value=pos, command=update_preview).grid(row=1, column=i, padx=5, pady=5)

# Add scale for watermark size
tk.Label(frame, text="Watermark Size (%)").grid(row=2, column=0, columnspan=2)
size = tk.IntVar(value=50)
size_scale = tk.Scale(frame, from_=10, to=100, orient="horizontal", variable=size, command=update_preview)
size_scale.grid(row=2, column=2, columnspan=3, padx=5, pady=5)

btn_save = tk.Button(frame, text="Save Image", command=save_image)
btn_save.grid(row=3, column=0, columnspan=5, pady=10)

img_label = tk.Label(root)
img_label.pack(padx=10, pady=10)

print_logo()
root.mainloop()
