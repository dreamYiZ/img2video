import os
import ffmpeg
from gtts import gTTS, gTTSError
from PIL import Image
from tell_story import get_description_and_tell_a_story

# 图片下载路径
DOWNLOAD_PATH = 'pexels-download/'
# 输出视频路径
OUTPUT_PATH = 'output/'
# 临时调整大小后的图片路径
RESIZED_PATH = 'resized-download/'

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)
if not os.path.exists(RESIZED_PATH):
    os.makedirs(RESIZED_PATH)

def resize_images(input_images, size):
    resized_images = []
    for img_path in input_images:
        img = Image.open(img_path)
        img = img.resize(size, Image.LANCZOS)
        resized_img_path = os.path.join(RESIZED_PATH, os.path.basename(img_path))
        img.save(resized_img_path)
        resized_images.append(resized_img_path)
    return resized_images

def generate_audio(text, output_path):
    try:
        tts = gTTS(text, lang='en')
        tts.save(output_path)
    except gTTSError as e:
        print(f"gTTS error: {e}. Skipping audio generation.")

def generate_video():
    descriptions = get_description_and_tell_a_story()

    # 将描述转换为语音并保存
    story_text = " ".join([item['story_part'] for item in descriptions])
    audio_path = os.path.join(OUTPUT_PATH, 'story.mp3')
    generate_audio(story_text, audio_path)

    # 创建字幕文件
    subtitle_path = os.path.join(OUTPUT_PATH, 'subtitles.srt')
    with open(subtitle_path, 'w') as subtitle_file:
        idx = 1
        time_offset = 0
        for item in descriptions:
            start_time = time_offset
            end_time = start_time + item['story_time'] * 60
            subtitle_file.write(f"{idx}\n")
            subtitle_file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            subtitle_file.write(f"{item['story_part']}\n\n")
            idx += 1
            time_offset = end_time

    # 将图片合成为视频并设置每张图片的持续时间
    input_images = [os.path.join(DOWNLOAD_PATH, item['filename']) for item in descriptions]
    resized_images = resize_images(input_images, (640, 480))  # 调整所有图片大小为640x480
    image_duration = time_offset / len(resized_images)  # 每张图片的持续时间
    intermediate_video_path = os.path.join(OUTPUT_PATH, 'intermediate.mp4')
    create_video(resized_images, image_duration, intermediate_video_path)

    # 添加音频和字幕到视频
    final_video_path = os.path.join(OUTPUT_PATH, 'output.mp4')
    add_audio_and_subtitles(intermediate_video_path, audio_path, subtitle_path, final_video_path)

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def create_video(input_images, image_duration, output_path):
    input_streams = [ffmpeg.input(img, framerate=1/duration) for img, duration in zip(input_images, [image_duration]*len(input_images))]
    video_stream = ffmpeg.concat(*input_streams, v=1, a=0).filter('fps', fps=30, round='up')
    video_stream.output(output_path).overwrite_output().run()

def add_audio_and_subtitles(video_path, audio_path, subtitle_path, output_path):
    video_stream = ffmpeg.input(video_path)
    audio_stream = ffmpeg.input(audio_path)
    ffmpeg.output(video_stream, audio_stream, output_path, vf=f'subtitles={subtitle_path}').overwrite_output().run()

def main():
    generate_video()

if __name__ == '__main__':
    main()
