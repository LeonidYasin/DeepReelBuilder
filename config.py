# config.py
import os

OUTPUT_DIR = "cloud_video_output"
LOCAL_MEDIA_DIR = "assets"          # папка с вашими файлами
MEDIA_SOURCE = "local"              # "local" или "pollinations" (если захотите вернуть)
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
MAX_SCENES = 100   # или любое число заведомо больше количества сцен
OUTPUT_VIDEO_NAME = "finished_cloud_video.mp4"
VIDEO_BITRATE = "5000k"
AUDIO_BITRATE = "192k"
FPS = 24
GPU_ENCODER = None
# Полностью отключить субтитры (True — субтитры есть, False — нет)
SHOW_SUBTITLES = False
# Эффект медленного отъезда камеры (зум-аут) для изображений
ZOOM_OUT_ENABLED = True
ZOOM_OUT_START_SCALE = 1.15   # во сколько раз увеличено изображение в начале (1.15 = +15%)
# Эффекты, применяемые к изображениям (zoom_out и будущие)
# Чтобы отключить эффект, просто удалите соответствующую строчку.
EFFECTS_CONFIG = {
    'zoom_out': {},   # можно передать параметры, но сейчас не нужно
}
