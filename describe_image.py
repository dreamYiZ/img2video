import os
import ollama

# 图片下载路径
DOWNLOAD_PATH = 'pexels-download/'


def describe_image(image_path):
    res = ollama.chat(
        model="llava:7b",
        messages=[
            {
                'role': 'user',
                'content': 'Describe this image:',
                'images': [image_path]
            }
        ]
    )
    if 'message' in res and 'content' in res['message']:
        return res['message']['content']
    else:
        return "No description available"


def process_images():
    if not os.path.exists(DOWNLOAD_PATH):
        print(f"Directory {DOWNLOAD_PATH} does not exist.")
        return []

    descriptions = []
    for filename in os.listdir(DOWNLOAD_PATH):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(DOWNLOAD_PATH, filename)
            description = describe_image(image_path)
            descriptions.append({'filename': filename, 'description': description})

    return descriptions


def main():
    descriptions = process_images()
    for item in descriptions:
        print(f"Image: {item['filename']}\nDescription: {item['description']}\n")


if __name__ == '__main__':
    main()
