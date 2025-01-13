
# Pexels图片下载器

这个脚本用于从Pexels网站下载图片并保存到本地文件夹中。

## 配置

1. 在项目根目录下创建一个`config.json`文件，并添加以下内容：
   ```json
   {
       "PEXEL_API_KEY": "your_api_key_here",
       "PER_PAGE": 5,
       "keyword": "cat"
   }
   ```

2. 将 `PEXEL_API_KEY` 放入环境变量中：
   ```bash
   export PEXEL_API_KEY=your_api_key_here
   ```

## 安装

首先，安装所需的依赖项：
```bash
pip install requests
```

## 运行

你可以使用以下命令运行程序并下载指定关键词的Pexels图片：

```bash
python download_pexels.py cat
```
或
```bash
python download_pexels.py [keyword]
```
将 `[keyword]` 替换为你想要搜索的关键字。

## 配置

你可以在`config.json`文件中写入配置。需要注意的是，环境变量与命令行参数的优先级更高。

### 配置示例

在`config.json`文件中，你可以添加如下配置：
```json
{
  "PEXEL_API_KEY": "your_api_key_here",
  "PER_PAGE": 10,
  "keyword": "nature",
  "output_directory": "./downloads"
}
```

### 运行示例

1. 使用环境变量设置API密钥并运行程序：
   ```bash
   export PEXEL_API_KEY=your_api_key_here
   python download_pexels.py dog
   ```

2. 使用命令行参数设置关键词：
   ```bash
   python download_pexels.py bird
   ```

3. 使用配置文件设置默认关键词并运行程序：
   ```bash
   python download_pexels.py
   ```


希望这些说明能够帮助你更好地理解和使用这个Python脚本。如果你有任何问题或需要进一步的帮助，请随时告诉我！
Downloading and Extracting Packages:

# conda
   
###    To activate this environment, use
   
        $ conda activate image2video
   
###    To deactivate an active environment, use
   
        $ conda deactivate



