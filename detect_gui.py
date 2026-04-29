"""
Детекция сундуков в режиме реального времени с отображением результатов в Tkinter.

Перед запуском установите зависимости:
    pip install ultralytics pillow pyautogui

Запуск:
    python detect_gui.py

Скрипт захватывает изображение экрана, запускает предсказание модели и
рисует найденные боксы. Период обновления задаётся параметром refresh_ms.
"""
import tkinter as tk
from PIL import Image, ImageTk, ImageGrab, ImageDraw
from ultralytics import YOLO


class ChestDetectorGUI:
    def __init__(self, model_path: str = "runs/chest/train/weights/best.pt", refresh_ms: int = 1000):
        self.model = YOLO(model_path)
        self.refresh_ms = refresh_ms

        self.root = tk.Tk()
        self.root.title("Детекция сундука Minecraft")
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.update_frame()
        self.root.mainloop()

    def update_frame(self):
        # Захват скриншота всего экрана
        screenshot = ImageGrab.grab()
        result = self.model.predict(source=screenshot, imgsz=640, conf=0.25, verbose=False)[0]
        # Копируем изображение для рисования
        img = screenshot.copy()
        draw = ImageDraw.Draw(img)
        for box, cls, conf in zip(result.boxes.xywh, result.boxes.cls, result.boxes.conf):
            if int(cls) == 0:
                x_center, y_center, w, h = box
                x1 = int(x_center - w / 2)
                y1 = int(y_center - h / 2)
                x2 = int(x_center + w / 2)
                y2 = int(y_center + h / 2)
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                draw.text((x1, y1 - 10), f"chest {conf:.2f}", fill="red")
        # Масштабируем изображение для отображения
        resized = img.resize((800, 600))
        self.photo = ImageTk.PhotoImage(resized)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(self.refresh_ms, self.update_frame)


if __name__ == "__main__":
    ChestDetectorGUI()
