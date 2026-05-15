# main.py
import sys
import time
import os
from config import MAX_SCENES, LOCAL_MEDIA_DIR, MEDIA_SOURCE
from script_reader import load_script
from media_provider import get_media_file
from audio_generator import generate_audio
from video_assembler import assemble_video

def main():
    if len(sys.argv) != 2:
        print("Использование: python main.py <файл_сценария.json|txt>")
        sys.exit(1)

    script_file = sys.argv[1]
    print(f"📄 Чтение сценария из {script_file}")
    try:
        scenes = load_script(script_file)
    except Exception as e:
        print(f"❌ Ошибка чтения: {e}")
        sys.exit(1)

    scenes = scenes[:MAX_SCENES]
    print(f"📜 Сцен: {len(scenes)}")

    # Проверяем наличие локальной папки
    if not os.path.isdir(LOCAL_MEDIA_DIR):
        print(f"❌ Папка '{LOCAL_MEDIA_DIR}' не найдена. Создайте её и поместите файлы сцен.")
        sys.exit(1)

    # Подготавливаем пути к медиа и озвучку
    for i, scene in enumerate(scenes):
        print(f"\n--- Сцена {i+1} ---")
        try:
            media_path, media_type = get_media_file(i)
            scene['media_path'] = media_path
            scene['media_type'] = media_type
            print(f"  📁 Найден файл: {os.path.basename(media_path)} ({media_type})")
        except FileNotFoundError as e:
            print(f"  ❌ {e}")
            sys.exit(1)

        scene['audio_path'] = generate_audio(scene['phrase'], i)
        # Можно добавить небольшую паузу, если TTS перегружается
        if i < len(scenes) - 1:
            time.sleep(2)

    assemble_video(scenes)

if __name__ == "__main__":
    main()