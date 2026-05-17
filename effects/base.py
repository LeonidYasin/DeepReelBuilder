# effects/base.py
class BaseEffect:
    """Базовый класс для эффектов, применяемых к клипам."""

    def __init__(self, **kwargs):
        # Сохраняем все параметры эффекта
        self.params = kwargs

    def apply(self, clip, duration, media_type):
        """
        Применяет эффект к клипу.

        :param clip: MoviePy-клип (ImageClip или VideoFileClip)
        :param duration: длительность сцены в секундах
        :param media_type: 'image' или 'video'
        :return: обработанный клип (может быть тот же или новый)
        """
        return clip
