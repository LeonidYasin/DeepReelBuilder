# resize_media.py
import os
from PIL import Image
from config import LOCAL_MEDIA_DIR, IMAGE_WIDTH, IMAGE_HEIGHT

def resize_all():
    if not os.path.isdir(LOCAL_MEDIA_DIR):
        print(f"Папка {LOCAL_MEDIA_DIR} не найдена")
        return
    for fname in sorted(os.listdir(LOCAL_MEDIA_DIR)):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(LOCAL_MEDIA_DIR, fname)
            try:
                img = Image.open(path).convert('RGB')
                if img.size != (IMAGE_WIDTH, IMAGE_HEIGHT):
                    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS)
                    img.save(path, quality=95)
                    print(f"  ✅ {fname} → {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
            except Exception as e:
                print(f"  ❌ {fname}: {e}")

if __name__ == "__main__":
    resize_all()
    print("Готово. Теперь можно запускать main.py")