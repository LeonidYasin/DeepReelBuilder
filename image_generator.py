# image_generator.py
import os
import time
import requests
from PIL import Image
from config import OUTPUT_DIR, IMAGE_WIDTH, IMAGE_HEIGHT

def download_image(prompt, index):
    """Генерирует изображение через Pollinations AI и сохраняет в OUTPUT_DIR."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img_path = os.path.join(OUTPUT_DIR, f"img_{index:02d}.jpg")
    encoded_prompt = requests.utils.quote(prompt, safe='')
    params = {
        "width": IMAGE_WIDTH,
        "height": IMAGE_HEIGHT,
        "model": "flux",
        "seed": 42 + index,
        "enhance": "true",
        "nologo": "true"
    }
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    print(f"  🖼️ Изображение {index+1}...")
    for attempt in range(2):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=120)
            if resp.status_code == 200 and 'image' in resp.headers.get('Content-Type', ''):
                with open(img_path, 'wb') as f:
                    f.write(resp.content)
                # Проверяем и конвертируем
                with Image.open(img_path) as test:
                    test.verify()
                img = Image.open(img_path).convert('RGB')
                if img.size != (IMAGE_WIDTH, IMAGE_HEIGHT):
                    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS)
                img.save(img_path, 'JPEG', quality=92, optimize=True)
                print(f"    ✅ {img.size[0]}×{img.size[1]}, {os.path.getsize(img_path)/1024:.0f} КБ")
                return img_path
            elif resp.status_code == 429:
                time.sleep(15)
            else:
                time.sleep(5)
        except:
            time.sleep(5)
    # Заглушка
    return _create_fallback(img_path, index)

def _create_fallback(img_path, index):
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=(20,20,30))
    img.save(img_path, 'JPEG')
    print(f"    ⬛ Заглушка {index+1}")
    return img_path