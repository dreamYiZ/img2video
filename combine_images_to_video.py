import os
import ffmpeg
import random
import yaml
from PIL import Image, ImageOps

# 读取 config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 图片下载路径
DOWNLOAD_PATH = 'pexels-download/'
# 输出视频路径
OUTPUT_PATH = 'output/'
# 音频文件夹路径
MUSIC_PATH = 'music/'
# 每张图片的显示时间（秒），从配置文件读取，如果没有就使用默认值6
IMAGE_DURATION = config.get('image2video', {}).get('IMAGE_DURATION', 6)
# 调整后的图片大小（手机竖屏尺寸），从配置文件读取，如果没有就使用默认值(1080, 1920)
IMAGE_SIZE = config.get('image2video', {}).get('IMAGE_SIZE', (1080, 1920))

# 将 IMAGE_SIZE 转换为元组
if isinstance(IMAGE_SIZE, str):
    IMAGE_SIZE = eval(IMAGE_SIZE)

# 准备临时调整大小后的图片路径
RESIZED_PATH = 'resized-download/'

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)
if not os.path.exists(RESIZED_PATH):
    os.makedirs(RESIZED_PATH)

def resize_images(input_images, size):
    resized_images = []
    for img_path in input_images:
        img = Image.open(img_path)
        img = ImageOps.pad(img, size, color='black')
        resized_img_path = os.path.join(RESIZED_PATH, os.path.basename(img_path))
        img.save(resized_img_path)
        resized_images.append(resized_img_path)
    return resized_images

def generate_video_from_images():
    input_images = sorted([os.path.join(DOWNLOAD_PATH, img) for img in os.listdir(DOWNLOAD_PATH) if img.endswith(('jpg', 'jpeg', 'png'))])

    if not input_images:
        print("No images found in the specified directory.")
        return

    # 调整所有图片的大小
    resized_images = resize_images(input_images, IMAGE_SIZE)

    # 打印出所有的resized_images，用来调试
    print("Resized images:")
    for img in resized_images:
        print(img)

    # 创建并保存每个视频文件
    temp_videos = []
    for i, img in enumerate(resized_images):
        temp_video_path = os.path.join(OUTPUT_PATH, f'{i}.mp4')
        ffmpeg.input(img, loop=1, t=IMAGE_DURATION).output(temp_video_path, vcodec='libx264', r=30, pix_fmt='yuv420p').overwrite_output().run()
        temp_videos.append(temp_video_path)

    print("Temporary video files created:")
    for temp_video in temp_videos:
        print(temp_video)

    # 创建视频
    video_path = os.path.join(OUTPUT_PATH, 'final_output.mp4')
    input_streams = [ffmpeg.input(video) for video in temp_videos]

    print('input_streams')
    print(input_streams)
    print('input_streams -end')

# todo: 在视频拼接之间，使用变黑的转场效果
    # 将视频文件连接在一起
    video_stream = ffmpeg.concat(*input_streams, v=1, a=0).filter('fps', fps=30, round='up')

    # 从music文件夹下随机选择一个mp3文件
    music_files = [os.path.join(MUSIC_PATH, mp3) for mp3 in os.listdir(MUSIC_PATH) if mp3.endswith('.mp3')]
    if not music_files:
        print("No music files found in the specified directory.")
        return

    selected_music = random.choice(music_files)
    print(f'Selected music: {selected_music}')

    # 获取视频的总时长
    video_duration = IMAGE_DURATION * len(resized_images)

    # 创建音频流并截取到与视频流相同的长度
    audio_stream = ffmpeg.input(selected_music).filter('atrim', duration=video_duration)

    # 合成视频和音频
    video_with_audio = ffmpeg.output(video_stream, audio_stream, video_path, vcodec='libx264', acodec='aac', r=30, pix_fmt='yuv420p').overwrite_output()
    ffmpeg.run(video_with_audio)

    print(f"Video created at {video_path}")

def main():
    generate_video_from_images()

if __name__ == '__main__':
    main()
