"""
Скрипт для обучения модели YOLO26 на датасете сундуков.

Перед запуском установите пакет ultralytics:
    pip install ultralytics

Запуск:
    python train.py

В результате обучения модель сохранится в директории `runs`.
"""
from ultralytics import YOLO


def main():
    # Загружаем маленькую модель YOLO26
    model = YOLO("yolo26n.pt")
    # Обучаем модель на нашем датасете
    model.train(
        data="chest.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        workers=8,
        project="runs/chest",
    )


if __name__ == "__main__":
    main()
