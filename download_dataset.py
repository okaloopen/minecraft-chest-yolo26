"""
Скрипт для скачивания изображений сундуков Minecraft и создания простых меток.

Используется библиотека `duckduckgo_search` для поиска картинок
по ключевому слову. Каждая картинка сохраняется в папке `data/images/train`.
После скачивания создётся файл меток в формате YOLO для класса `chest`.

Запуск:
    python download_dataset.py

"""
import os
import requests
from typing import List

try:
    # duckduckgo_search нужен для поиска картинок. Установите: pip install duckduckgo_search
    from duckduckgo_search import ddg_images
except ImportError:
    raise ImportError(
        "Не удалось импортировать duckduckgo_search. Установите его командой `pip install duckduckgo_search`."
    )


def download_images(query: str, max_images: int = 500, out_dir: str = "data/images/train") -> List[str]:
    """Скачивает изображения по ключевому слову.

    Args:
        query: поисковый запрос.
        max_images: максимальное количество картинок.
        out_dir: папка для сохранения.

    Returns:
        Список путей к скачанным файлам.
    """
    os.makedirs(out_dir, exist_ok=True)
    results = ddg_images(keywords=query, safesearch="Moderate", max_results=max_images)
    saved_paths = []
    for idx, res in enumerate(results):
        url = res.get("image")
        if not url:
            continue
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
            fname = f"chest_{idx:03d}{ext}"
            fpath = os.path.join(out_dir, fname)
            with open(fpath, "wb") as f:
                f.write(response.content)
            saved_paths.append(fpath)
            print(f"Скачано: {fpath}")
        except Exception as e:
            print(f"Не удалось скачать {url}: {e}")
    return saved_paths


def create_labels(image_paths: List[str], label_dir: str = "data/labels/train") -> None:
    """Создаёт файлы разметки с одним боксом на всё изображение.

    Координаты YOLO: class_id x_center y_center width height (нормализованы).
    """
    os.makedirs(label_dir, exist_ok=True)
    for image_path in image_paths:
        base = os.path.splitext(os.path.basename(image_path))[0]
        label_path = os.path.join(label_dir, base + ".txt")
        with open(label_path, "w") as f:
            # class_id=0, bbox охватывает весь кадр
            f.write("0 0.5 0.5 1.0 1.0\n")
        print(f"Создан файл метки: {label_path}")


if __name__ == "__main__":
    images = download_images("minecraft chest different angles", max_images=500)
    create_labels(images)
