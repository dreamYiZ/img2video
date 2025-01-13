import os
import subprocess
import sys


def run_script(script_path, *args):
    result = subprocess.run(['python', script_path] + list(args), capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        print(f"Error executing {script_path}")
        exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python combine_scripts.py <keyword>")
        exit(1)

    keyword = sys.argv[1]

    # 执行第一个脚本，并传递参数
    print("Running download_images.py script...")
    run_script('download_pexels.py', keyword)

    # 执行第二个脚本
    print("Running generate_video.py script...")
    run_script('combine_images_to_video.py')


if __name__ == '__main__':
    main()
