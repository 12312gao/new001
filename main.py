import requests
import json
import os
from datetime import datetime

class FirecrawlApp:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('FIRECRAWL_API_KEY')
        if not self.api_key:
            raise ValueError("API密钥未提供，请设置FIRECRAWL_API_KEY环境变量或在初始化时提供")
        
        self.base_url = "https://api.firecrawl.dev"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def crawl_url(self, url, options=None):
        """抓取指定URL的内容"""
        endpoint = f"{self.base_url}/crawl"
        
        payload = {"url": url}
        if options:
            payload.update(options)
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API请求错误: {e}")
            return None
    
    def extract_manga_data(self, response_data):
        """从API响应中提取漫画数据"""
        if not response_data or 'markdown' not in response_data:
            return None
        
        # 解析markdown内容，提取漫画信息
        markdown_content = response_data['markdown']
        
        # 提取标题、作者、描述等信息
        manga_data = {
            'title': self._extract_field(markdown_content, '标题'),
            'author': self._extract_field(markdown_content, '作者'),
            'description': self._extract_field(markdown_content, '描述'),
            'chapters': self._extract_chapters(markdown_content),
            'cover_url': self._extract_image_url(markdown_content),
            'tags': self._extract_tags(markdown_content)
        }
        
        return manga_data
    
    def _extract_field(self, markdown, field_name):
        """从markdown中提取指定字段的值"""
        import re
        pattern = rf"{field_name}[：:]\s*([^\n]+)"
        match = re.search(pattern, markdown)
        return match.group(1).strip() if match else ""
    
    def _extract_chapters(self, markdown):
        """提取漫画章节列表"""
        import re
        chapters = []
        
        # 匹配章节列表，格式可能是：第X章：章节名 或 第X话：章节名
        chapter_pattern = r"第(\d+)[章话]：?([^\n]+)"
        matches = re.finditer(chapter_pattern, markdown)
        
        for match in matches:
            chapter_num = match.group(1)
            chapter_title = match.group(2).strip()
            chapters.append({
                'number': int(chapter_num),
                'title': chapter_title
            })
        
        return chapters
    
    def _extract_image_url(self, markdown):
        """提取封面图片URL"""
        import re
        # 匹配markdown中的图片链接格式：![alt](url)
        pattern = r"!\[[^\]]*\]\(([^\)]+)\)"
        match = re.search(pattern, markdown)
        return match.group(1) if match else ""
    
    def _extract_tags(self, markdown):
        """提取漫画标签"""
        import re
        # 匹配标签格式，可能是：标签：tag1, tag2, tag3 或 类型：tag1/tag2/tag3
        pattern = r"(标签|类型)[：:]\s*([^\n]+)"
        match = re.search(pattern, markdown)
        
        if match:
            tags_str = match.group(2).strip()
            # 处理不同的分隔符
            if ',' in tags_str:
                return [tag.strip() for tag in tags_str.split(',')]
            elif '/' in tags_str:
                return [tag.strip() for tag in tags_str.split('/')]
            else:
                return [tags_str]
        return []
    
    def save_manga_data(self, manga_data, output_file=None):
        """将漫画数据保存到JSON文件"""
        if not manga_data:
            print("没有数据可保存")
            return False
        
        if not output_file:
            # 使用漫画标题作为文件名
            title = manga_data.get('title', 'unknown')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{title}_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(manga_data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {output_file}")
            return True
        except Exception as e:
            print(f"保存数据时出错: {e}")
            return False

# 示例使用
def main():
    # 使用提供的API密钥
    api_key = 'fc-6019608aa5034733ba290644cf399fce'
    
    # 初始化FirecrawlApp
    app = FirecrawlApp(api_key)
    
    # 爱奇艺漫画URL - 使用真实的漫画ID
    manga_url = "https://www.iqiyi.com/manhua/19rqm98lxl"
    
    # 设置抓取选项
    options = {
        "wait": 2000,  # 等待页面加载的时间（毫秒）
        "javascript": True,  # 启用JavaScript
        "format": "markdown"  # 返回markdown格式的内容
    }
    
    print(f"正在抓取: {manga_url}")
    response_data = app.crawl_url(manga_url, options)
    
    if response_data:
        print("抓取成功，正在提取数据...")
        manga_data = app.extract_manga_data(response_data)
        
        if manga_data:
            print("数据提取成功:")
            print(f"标题: {manga_data['title']}")
            print(f"作者: {manga_data['author']}")
            print(f"标签: {', '.join(manga_data['tags'])}")
            print(f"章节数: {len(manga_data['chapters'])}")
            
            # 保存数据
            app.save_manga_data(manga_data)
        else:
            print("无法从响应中提取漫画数据")
    else:
        print("抓取失败")

if __name__ == "__main__":
    main()