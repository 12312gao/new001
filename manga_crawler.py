import argparse
import os
import sys
from main import FirecrawlApp

def setup_parser():
    """设置命令行参数解析器"""
    parser = argparse.ArgumentParser(description='爱奇艺漫画抓取工具')
    parser.add_argument('url', help='爱奇艺漫画页面URL')
    parser.add_argument('-k', '--api-key', help='Firecrawl API密钥（也可通过FIRECRAWL_API_KEY环境变量设置）')
    parser.add_argument('-o', '--output', help='输出文件路径（默认使用漫画标题和时间戳）')
    parser.add_argument('-w', '--wait', type=int, default=2000, help='页面加载等待时间（毫秒，默认2000）')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()
    
    # 获取API密钥（优先使用命令行参数，其次使用环境变量）
    api_key = args.api_key or os.environ.get('FIRECRAWL_API_KEY')
    if not api_key:
        print("错误: 未提供API密钥，请使用--api-key参数或设置FIRECRAWL_API_KEY环境变量")
        sys.exit(1)
    
    # 初始化应用
    try:
        app = FirecrawlApp(api_key)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    # 设置抓取选项
    options = {
        "wait": args.wait,
        "javascript": True,
        "format": "markdown"
    }
    
    print(f"正在抓取: {args.url}")
    response_data = app.crawl_url(args.url, options)
    
    if not response_data:
        print("抓取失败，请检查URL和API密钥是否正确")
        sys.exit(1)
    
    if args.verbose:
        print("API响应:")
        print(response_data)
    
    print("抓取成功，正在提取数据...")
    manga_data = app.extract_manga_data(response_data)
    
    if not manga_data:
        print("无法从响应中提取漫画数据，请检查页面格式是否支持")
        sys.exit(1)
    
    # 显示提取的数据
    print("\n漫画信息:")
    print(f"标题: {manga_data['title']}")
    print(f"作者: {manga_data['author']}")
    print(f"标签: {', '.join(manga_data['tags'])}")
    print(f"章节数: {len(manga_data['chapters'])}")
    
    if manga_data['cover_url']:
        print(f"封面图片: {manga_data['cover_url']}")
    
    # 保存数据
    app.save_manga_data(manga_data, args.output)
    
    print("\n抓取完成!")

if __name__ == "__main__":
    main()