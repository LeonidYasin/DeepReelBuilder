# audio_generator.py
import os
import asyncio
import edge_tts
from moviepy import AudioFileClip
from config import OUTPUT_DIR

async def _generate_tts(text, output_path, voice="ru-RU-DmitryNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_audio(text, index):
    """Озвучивает фразу через edge-tts, возвращает путь к mp3."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"audio_{index:02d}.mp3")
    clean_text = text.replace('"', '').replace("'", "").replace('«', '').replace('»', '')
    print(f"  🔊 Озвучка {index+1}...")
    try:
        asyncio.run(_generate_tts(clean_text, output_path))
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"    ✅ Аудио {index+1}")
            return output_path
    except Exception as e:
        print(f"    ⚠️ Ошибка: {e}")
    # Тихая заглушка
    try:
        AudioFileClip.audio_clip_array_duration(1).write_audiofile(output_path, fps=44100, logger=None)
    except:
        with open(output_path, 'wb') as f:
            f.write(b'\x00' * 10000)
    return output_path