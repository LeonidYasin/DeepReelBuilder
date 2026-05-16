# video_assembler.py
import os
import time
import subprocess
import platform
from moviepy import (
    ImageClip, AudioFileClip, TextClip, VideoFileClip,
    CompositeVideoClip, concatenate_videoclips, ColorClip
)
from config import (
    OUTPUT_DIR, IMAGE_WIDTH, IMAGE_HEIGHT, OUTPUT_VIDEO_NAME,
    FPS, VIDEO_BITRATE, AUDIO_BITRATE, GPU_ENCODER, SHOW_SUBTITLES
)
from font_finder import find_font

FONT_PATH = find_font()

def _detect_gpu_encoder():
    if GPU_ENCODER:
        enc = GPU_ENCODER.lower()
        if enc == 'nvenc':
            return 'nvenc', ['-preset', 'p4', '-tune', 'hq']
        elif enc == 'amf':
            return 'amf', ['-quality', 'balanced']
        elif enc == 'qsv':
            return 'qsv', ['-preset', 'medium']
    try:
        creationflags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        res = subprocess.run(['ffmpeg', '-encoders'], capture_output=True,
                             text=True, timeout=5, creationflags=creationflags)
        if 'h264_nvenc' in res.stdout:
            return 'nvenc', ['-preset', 'p4', '-tune', 'hq']
        elif 'h264_amf' in res.stdout:
            return 'amf', ['-quality', 'balanced']
        elif 'h264_qsv' in res.stdout:
            return 'qsv', ['-preset', 'medium']
    except:
        pass
    return 'cpu', ['-preset', 'medium', '-crf', '23', '-tune', 'film']

def _create_subtitle(text, duration):
    """Создаёт текстовый клип с авто-переносом и ограничением высоты."""
    if not SHOW_SUBTITLES:
        return None
    try:
        txt = TextClip(
            text=text,
            font=FONT_PATH,
            font_size=36,                   # уменьшенный шрифт
            color='white',
            stroke_color='black',
            stroke_width=2,
            method='caption',
            size=(IMAGE_WIDTH * 0.85, None),  # ширина 85% экрана
            text_align='center'
        ).with_duration(duration)
        # Ограничиваем высоту одной трети экрана
        if txt.h > IMAGE_HEIGHT * 0.35:
            txt = txt.resized(height=IMAGE_HEIGHT * 0.35)
        return txt
    except Exception as e:
        print(f"⚠️ Ошибка при создании текста: {e}")
        return TextClip(
            text="[шрифт не найден]",
            font_size=36,
            color='red',
            method='caption',
            size=(IMAGE_WIDTH * 0.85, None),
            text_align='center'
        ).with_duration(duration)

def _create_subtitle_background(txt_clip, duration):
    """Полупрозрачный фон точно по размеру текста (если текст есть)."""
    if txt_clip is None:
        return None
    padding = 20
    bg_width = int(txt_clip.w + padding * 2)
    bg_height = int(txt_clip.h + padding * 2)
    return ColorClip(
        size=(bg_width, bg_height),
        color=(0, 0, 0)
    ).with_opacity(0.65).with_duration(duration)


def assemble_video(scenes):
    if not scenes:
        print("❌ Нет сцен для видео")
        return

    print(f"\n🎬 Сборка {len(scenes)} сцен...")
    clips = []

    for i, scene in enumerate(scenes):
        phrase = scene['phrase']
        media_path = scene['media_path']
        media_type = scene['media_type']
        audio_path = scene['audio_path']

        print(f"\n📽️ Сцена {i+1}: \"{phrase[:80]}...\"")

        # Аудио
        try:
            audio = AudioFileClip(audio_path)
            duration = max(audio.duration, 2.0)
        except:
            duration = 3.0
            audio = None

        # Медиа
        try:
            if media_type == 'video':
                clip = VideoFileClip(media_path).without_audio()
                if clip.duration < duration:
                    last_frame = clip.to_ImageClip(clip.duration - 0.1 if clip.duration > 0.1 else 0)
                    remaining = duration - clip.duration
                    freeze = last_frame.with_duration(remaining)
                    clip = concatenate_videoclips([clip, freeze])
                elif clip.duration > duration:
                    clip = clip.subclipped(0, duration)
            else:
                clip = ImageClip(media_path).with_duration(duration)
        except Exception as e:
            print(f"    ⚠️ Ошибка загрузки медиа: {e}")
            clip = ColorClip(size=(IMAGE_WIDTH, IMAGE_HEIGHT), color=(20, 20, 30)).with_duration(duration)

        # Масштабирование
        target_ratio = IMAGE_WIDTH / IMAGE_HEIGHT
        clip_ratio = clip.w / clip.h
        if clip_ratio > target_ratio:
            clip = clip.resized(height=IMAGE_HEIGHT)
        else:
            clip = clip.resized(width=IMAGE_WIDTH)
        clip = clip.with_position('center')

        # Субтитры
        if SHOW_SUBTITLES:
            txt = _create_subtitle(phrase, duration)
            bg = _create_subtitle_background(txt, duration)
            if txt is not None and bg is not None:
                layers = [clip, bg, txt.with_position(('center', IMAGE_HEIGHT - (bg.h // 2) - 40))]
            else:
                layers = [clip]
        else:
            layers = [clip]

        final_clip = CompositeVideoClip(layers, size=(IMAGE_WIDTH, IMAGE_HEIGHT))
        if audio:
            final_clip = final_clip.with_audio(audio)

        clips.append(final_clip)
        print(f"    ✅ Готово")

    if not clips:
        return

    encoder_name, _ = _detect_gpu_encoder()
    total_dur = sum(c.duration for c in clips)
    print(f"\n🧩 Склейка (кодер: {encoder_name}), длительность: {total_dur:.1f} с")

    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        codec = 'libx264'
        ffmpeg_params = ['-preset', 'medium', '-crf', '23', '-tune', 'film']
    elif encoder_name == 'nvenc':
        codec = 'h264_nvenc'
        ffmpeg_params = ['-preset', 'p4', '-tune', 'hq']
    elif encoder_name == 'amf':
        codec = 'h264_amf'
        ffmpeg_params = ['-quality', 'balanced']
    elif encoder_name == 'qsv':
        codec = 'h264_qsv'
        ffmpeg_params = ['-preset', 'medium']
    else:
        codec = 'libx264'
        ffmpeg_params = ['-preset', 'medium', '-crf', '23', '-tune', 'film']

    final_video = concatenate_videoclips(clips, method="compose")
    output_path = OUTPUT_VIDEO_NAME
    t0 = time.time()
    final_video.write_videofile(
        output_path, fps=FPS, codec=codec, audio_codec="aac",
        bitrate=VIDEO_BITRATE, audio_bitrate=AUDIO_BITRATE,
        temp_audiofile="temp-audio.m4a", remove_temp=True,
        ffmpeg_params=ffmpeg_params, logger='bar'
    )
    elapsed = time.time() - t0
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n✅ Готово: {output_path} ({size_mb:.1f} МБ) за {elapsed:.1f} с")
