# effects/zoom_out.py
from .base import BaseEffect
from config import IMAGE_WIDTH, IMAGE_HEIGHT


class ZoomOutEffect(BaseEffect):
    """
    Плавный зум-аут от размера «по ширине» до размера «по высоте».
    Работает только с изображениями.
    """

    def apply(self, clip, duration, media_type):
        if media_type != 'image' or duration <= 0:
            # Для видео или нулевой длительности эффект не применяется
            return clip

        orig_w, orig_h = clip.w, clip.h
        scale_width = IMAGE_WIDTH / orig_w
        scale_height = IMAGE_HEIGHT / orig_h

        def zoom_func(t, sw=scale_width, sh=scale_height, dur=duration):
            return sw - (sw - sh) * (t / dur)

        return clip.resized(zoom_func).with_position('center')
