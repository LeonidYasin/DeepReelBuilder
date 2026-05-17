# effects/dispatcher.py
from .zoom_out import ZoomOutEffect


# Словарь, связывающий названия эффектов с их классами
AVAILABLE_EFFECTS = {
    'zoom_out': ZoomOutEffect,
}


def apply_effects(clip, duration, media_type, effects_config):
    """
    Применяет к клипу все включённые эффекты.

    :param clip: MoviePy-клип
    :param duration: длительность сцены
    :param media_type: 'image' или 'video'
    :param effects_config: словарь с настройками эффектов (из config.py)
    :return: обработанный клип
    """
    for effect_name, effect_params in effects_config.items():
        if effect_name in AVAILABLE_EFFECTS:
            effect_class = AVAILABLE_EFFECTS[effect_name]
            # Создаём экземпляр эффекта с переданными параметрами
            effect_instance = effect_class(**effect_params)
            clip = effect_instance.apply(clip, duration, media_type)
    return clip
