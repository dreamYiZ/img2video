import os
import requests
import yaml
import shutil

# 读取 config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 从环境变量或config文件读取配置信息
PEXEL_API_KEY = os.getenv('PEXEL_API_KEY') or config.get('pexels', {}).get('PEXEL_API_KEY')
PER_PAGE = os.getenv('PER_PAGE') or config.get('pexels', {}).get('PER_PAGE') or 5  # 优先级: env > config > 默认值
keyword = (len(os.sys.argv) > 1 and os.sys.argv[1]) or os.getenv('KEYWORD') or config.get('pexels', {}).get('keyword') or 'cat'  # 优先级: 命令行参数 > env > config > 默认值
size = os.getenv('SIZE') or config.get('pexels', {}).get('size') or 'medium'  # 新增配置选项

print(f'[PEXEL_API_KEY] --> {PEXEL_API_KEY}')
print(f'[PER_PAGE] --> {PER_PAGE}')
print(f'[keyword] --> {keyword}')
print(f'[size] --> {size}')

DOWNLOAD_PATH = 'pexels-download/'

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

BASE_API_PATH = 'https://api.pexels.com/v1/'
API_SEARCH = BASE_API_PATH + 'search'

def base_request(url, method="GET"):
    headers = {
        'Authorization': PEXEL_API_KEY,
    }
    return requests.request(method, url, headers=headers)

def search_photo(options):
    query_string = '&'.join([f"{key}={value}" for key, value in options.items()])
    url = f"{API_SEARCH}?{query_string}"
    return base_request(url)

def download(uri, filename, callback):
    response = requests.get(uri, stream=True)
    if response.status_code == 200:
        with open(os.path.join(DOWNLOAD_PATH, filename), 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        callback()

def get_file_name_by_url(url):
    # 去掉问号后的内容
    return url.split('/').pop().split('?')[0]

def empty_download_folder():
    for filename in os.listdir(DOWNLOAD_PATH):
        file_path = os.path.join(DOWNLOAD_PATH, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def start_search_and_download():
    response = search_photo({'query': keyword, 'per_page': PER_PAGE})
    photos = response.json().get('photos', [])
    for photo in photos:
        print(photo['src'][size])  # 使用选择的图片大小下载
        download(photo['src'][size], get_file_name_by_url(photo['src'][size]), lambda: None)

def main():
    empty_download_folder()
    start_search_and_download()

if __name__ == '__main__':
    main()
