# media_provider.py
import os
from config import LOCAL_MEDIA_DIR, IMAGE_WIDTH, IMAGE_HEIGHT, OUTPUT_DIR

def get_media_file(index):
    """
    Ищет локальный файл сцены по индексу в папке LOCAL_MEDIA_DIR.
    Поддерживаемые расширения: .jpg, .jpeg, .png, .mp4, .webm.
    Приоритет: видео > изображение.
    Возвращает кортеж (путь, тип: 'image' или 'video').
    Если файл не найден, генерирует исключение с понятным сообщением.
    """
    base_name = f"scene_{index:02d}"
    extensions = ['.mp4', '.webm', '.jpg', '.jpeg', '.png']
    
    for ext in extensions:
        file_path = os.path.join(LOCAL_MEDIA_DIR, base_name + ext)
        if os.path.isfile(file_path):
            media_type = 'video' if ext in ('.mp4', '.webm') else 'image'
            return file_path, media_type
    
    raise FileNotFoundError(
        f"Не найден локальный файл для сцены {index}.\n"
        f"Ожидаемое имя: {base_name}.(jpg/png/mp4) в папке '{LOCAL_MEDIA_DIR}'.\n"
        f"Поместите туда изображение или видео, созданное вручную по промпту из сценария."
    )