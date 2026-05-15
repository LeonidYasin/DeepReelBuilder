# script_reader.py
import json
import sys

def load_script(file_path):
    """
    Читает сценарий из JSON или текстового файла.
    Возвращает список словарей [{phrase, image_prompt}, ...].
    """
    if not file_path.lower().endswith(('.json', '.txt')):
        raise ValueError("Поддерживаются только .json и .txt файлы")

    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'scenes' not in data:
            raise KeyError("JSON должен содержать ключ 'scenes' с массивом объектов")
        scenes = data['scenes']
        # Проверяем структуру
        for i, scene in enumerate(scenes):
            if 'phrase' not in scene or 'image_prompt' not in scene:
                raise ValueError(f"Сцена {i+1}: отсутствует 'phrase' или 'image_prompt'")
        return scenes

    elif file_path.endswith('.txt'):
        scenes = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '|' not in line:
                    continue
                phrase, img_prompt = line.split('|', 1)
                scenes.append({
                    'phrase': phrase.strip(),
                    'image_prompt': img_prompt.strip()
                })
        return scenes