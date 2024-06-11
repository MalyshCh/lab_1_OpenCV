import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Инициализация параметров
canny_min_val = 50
canny_max_val = 150
binary_thresh = 128

# Глобальная переменная для хранения текущего изображения
current_frame = None

# Функции для обработки слайдеров
def adjust_canny_min(value):
    global canny_min_val
    canny_min_val = int(value)
    if current_frame is not None:
        render_image(current_frame)

def adjust_canny_max(value):
    global canny_max_val
    canny_max_val = int(value)
    if current_frame is not None:
        render_image(current_frame)

def adjust_binary_thresh(value):
    global binary_thresh
    binary_thresh = int(value)
    if current_frame is not None:
        render_image(current_frame)

def choose_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        load_image(file_path)

def choose_video():
    file_path = filedialog.askopenfilename()
    if file_path:
        play_video(file_path)

def launch_webcam():
    play_video(0)

def load_image(file_path):
    global current_frame
    img = cv2.imread(file_path)
    if img is not None:
        current_frame = img
        render_image(img)

def play_video(source):
    global current_frame
    current_frame = None
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Ошибка: Невозможно открыть источник видео.")
        return

    def fetch_frame():
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return
        render_image(frame)
        root.after(10, fetch_frame)

    fetch_frame()

def render_image(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_frame, canny_min_val, canny_max_val)
    _, binary = cv2.threshold(gray_frame, binary_thresh, 255, cv2.THRESH_BINARY)

    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    binary_colored = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    display_images(edges_colored, binary_colored)

def display_images(left_image, right_image):
    left_resized = cv2.resize(left_image, (400, 400))
    right_resized = cv2.resize(right_image, (400, 400))

    left_img_pil = Image.fromarray(left_resized)
    right_img_pil = Image.fromarray(right_resized)

    left_imgtk = ImageTk.PhotoImage(image=left_img_pil)
    right_imgtk = ImageTk.PhotoImage(image=right_img_pil)

    display_panel_left.imgtk = left_imgtk
    display_panel_left.configure(image=left_imgtk)

    display_panel_right.imgtk = right_imgtk
    display_panel_right.configure(image=right_imgtk)

# Создание графического интерфейса с использованием tkinter
root = tk.Tk()
root.title("Приложение для фильтрации видео")
root.configure(bg="#f0f0f0")

# Основной фрейм
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(padx=10, pady=10)

# Левое изображение
display_panel_left = tk.Label(main_frame, bg="#d9d9d9")
display_panel_left.grid(row=0, column=0)

# Панель управления
control_panel = tk.Frame(main_frame, bg="#f0f0f0")
control_panel.grid(row=0, column=1, padx=10)

btn_style = {
    "bg": "#4CAF50",
    "fg": "white",
    "font": ("Arial", 12, "bold"),
    "relief": tk.RAISED,
    "bd": 3,
    "width": 20,
    "height": 2
}

btn_open_image = tk.Button(control_panel, text="Загрузить изображение", command=choose_image, **btn_style)
btn_open_image.pack(pady=10)

btn_open_video = tk.Button(control_panel, text="Загрузить видео", command=choose_video, **btn_style)
btn_open_video.pack(pady=10)

btn_start_webcam = tk.Button(control_panel, text="Запустить веб-камеру", command=launch_webcam, **btn_style)
btn_start_webcam.pack(pady=10)

slider_style = {
    "orient": tk.HORIZONTAL,
    "length": 300,
    "width": 15,
    "sliderlength": 20,
    "bg": "#f0f0f0",
    "highlightbackground": "#f0f0f0",
    "highlightthickness": 0,
    "bd": 0
}

slider_canny_min = tk.Scale(control_panel, from_=0, to=255, label="Canny Threshold", command=adjust_canny_min, **slider_style)
slider_canny_min.set(canny_min_val)
slider_canny_min.pack(pady=10)

slider_canny_max = tk.Scale(control_panel, from_=0, to=255, label="Canny Linking", command=adjust_canny_max, **slider_style)
slider_canny_max.set(canny_max_val)
slider_canny_max.pack(pady=10)

slider_binary = tk.Scale(control_panel, from_=0, to=255, label="Threshold", command=adjust_binary_thresh, **slider_style)
slider_binary.set(binary_thresh)
slider_binary.pack(pady=10)

# Правое изображение
display_panel_right = tk.Label(main_frame, bg="#d9d9d9")
display_panel_right.grid(row=0, column=2)

root.mainloop()
