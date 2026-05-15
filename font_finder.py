# font_finder.py
import platform
import os
import glob

def find_font():
    # 1. Ищем в текущей папке (можно положить arial.ttf вручную)
    local_candidates = ['arial.ttf', 'Arial.ttf', 'font.ttf']
    for name in local_candidates:
        if os.path.isfile(name):
            return os.path.abspath(name)

    system = platform.system()
    if system == "Windows":
        fonts_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
        # Приоритетные шрифты с поддержкой кириллицы
        preferred = ['arial.ttf', 'calibri.ttf', 'segoeui.ttf', 'tahoma.ttf', 'verdana.ttf']
        for font_name in preferred:
            full_path = os.path.join(fonts_dir, font_name)
            if os.path.isfile(full_path):
                return full_path
        # Если не нашли – берём первый попавшийся .ttf
        for f in glob.glob(os.path.join(fonts_dir, '*.ttf')):
            return f
    elif system == "Darwin":
        for path in ['/System/Library/Fonts/Helvetica.ttc', '/Library/Fonts/Arial.ttf']:
            if os.path.isfile(path):
                return path
    else:  # Linux (Ubuntu, etc.)
         return "DejaVu-Sans"
    return None
