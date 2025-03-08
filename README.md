# 爱奇艺漫画抓取工具

这是一个使用Firecrawl API抓取爱奇艺漫画页面内容的工具，可以提取漫画的标题、作者、标签、章节列表等信息，并将其保存为JSON格式。

## 功能特点

- 自动抓取爱奇艺漫画页面内容
- 提取漫画基本信息（标题、作者、描述等）
- 提取漫画章节列表
- 提取漫画标签
- 提取漫画封面图片URL
- 将数据保存为JSON格式文件

## 安装要求

- Python 3.6+
- requests库

安装依赖：

```bash
pip install requests
```

## 使用方法

### 1. 获取Firecrawl API密钥

在使用本工具前，您需要获取Firecrawl API的密钥。

### 2. 设置API密钥

您可以通过以下两种方式设置API密钥：

- 设置环境变量：
  ```bash
  # Windows
  set FIRECRAWL_API_KEY=您的API密钥
  
  # Linux/Mac
  export FIRECRAWL_API_KEY=您的API密钥
  ```

- 使用命令行参数：
  ```bash
  python manga_crawler.py 漫画URL -k 您的API密钥
  ```

### 3. 运行工具

```bash
python manga_crawler.py https://www.iqiyi.com/manhua/漫画ID
```

### 命令行参数

```
python manga_crawler.py [-h] [-k API_KEY] [-o OUTPUT] [-w WAIT] [-v] url
```

- `url`：爱奇艺漫画页面URL（必需）
- `-k, --api-key`：Firecrawl API密钥
- `-o, --output`：输出文件路径（默认使用漫画标题和时间戳）
- `-w, --wait`：页面加载等待时间（毫秒，默认2000）
- `-v, --verbose`：显示详细信息
- `-h, --help`：显示帮助信息

## 示例

```bash
# 基本使用
python manga_crawler.py https://www.iqiyi.com/manhua/123456

# 指定API密钥
python manga_crawler.py https://www.iqiyi.com/manhua/123456 -k your_api_key

# 指定输出文件
python manga_crawler.py https://www.iqiyi.com/manhua/123456 -o my_manga.json

# 显示详细信息
python manga_crawler.py https://www.iqiyi.com/manhua/123456 -v

# 设置页面加载等待时间
python manga_crawler.py https://www.iqiyi.com/manhua/123456 -w 3000
```

## 输出示例

```json
{
  "title": "漫画标题",
  "author": "作者名",
  "description": "漫画描述...",
  "chapters": [
    {"number": 1, "title": "第一章标题"},
    {"number": 2, "title": "第二章标题"}
  ],
  "cover_url": "https://example.com/cover.jpg",
  "tags": ["标签1", "标签2"]
}
```

## 注意事项

- 本工具仅用于学习和研究目的
- 请遵守爱奇艺的使用条款和服务协议
- 请合理设置抓取频率，避免对目标网站造成过大负担

## 许可证

MIT License