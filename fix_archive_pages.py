#!/usr/bin/env python3
"""
修复 tech 归档页：添加背景图、导航、修复路径
"""

import re
from pathlib import Path
from datetime import datetime

BLOG_PATH = Path("/home/swg/.openclaw/workspace/tech")
HISTORY_DIR = BLOG_PATH / "history"

# 正确的 CSS 和 navbar 模板
NAVBAR_HTML = '''
    <nav class="navbar">
        <a href="../../../index.html" class="navbar-brand">📚 技术文档</a>
        <ul class="nav-links">
            <li><a href="../../../index.html" class="active">首页</a></li>
            <li><a href="../../../history.html">历史归档</a></li>
            <li><a href="../../../about.html">关于我们</a></li>
            <li><a href="../../../contact.html">联系我们</a></li>
        </ul>
    </nav>
'''

CSS_TEMPLATE = '''
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --container-bg: white;
            --text-color: #333;
            --nav-bg: white;
            --nav-text: #333;
            --border-color: rgba(0,0,0,0.1);
            --bg-image: url('../../../images/website-background-8k.png');
        }
        .dark-mode {
            --bg-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            --container-bg: #1a1a2e;
            --text-color: #e0e0e0;
            --nav-bg: #1f1f38;
            --nav-text: #e0e0e0;
            --border-color: rgba(255,255,255,0.1);
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-image) no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            padding: 20px;
            color: var(--text-color);
        }
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(255, 255, 255, 0.88);
            z-index: -1;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: var(--container-bg);
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            background: var(--nav-bg);
            border-bottom: 1px solid var(--border-color);
        }
        .navbar-brand {
            font-size: 1.5em;
            font-weight: bold;
            color: var(--nav-text);
            text-decoration: none;
        }
        .nav-links {
            display: flex;
            gap: 20px;
            list-style: none;
        }
        .nav-links a {
            color: var(--nav-text);
            text-decoration: none;
        }
        .nav-links a:hover, .nav-links a.active {
            color: #667eea;
        }
        .hero {
            background: var(--bg-gradient);
            color: white;
            padding: 50px 30px;
            text-align: center;
        }
        .hero h1 { font-size: 2.2em; margin-bottom: 15px; }
        .hero p { font-size: 1.1em; opacity: 0.9; }
        .hero-date { margin-top: 15px; font-size: 0.9em; opacity: 0.8; }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: background 0.3s;
        }
        .back-link:hover { background: rgba(255,255,255,0.3); }
        .content { padding: 40px 30px; }
        .content h2 {
            font-size: 1.8em;
            margin: 30px 0 15px 0;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }
        .content p { margin-bottom: 15px; line-height: 1.8; }
        .content pre {
            background: #f6f8fa;
            border-radius: 8px;
            padding: 15px;
            overflow-x: auto;
            margin: 15px 0;
        }
        .content img { max-width: 100%; border-radius: 8px; margin: 15px 0; }
        .footer {
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 0.9em;
            border-top: 1px solid var(--border-color);
        }
        .article-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .article-card h3 { color: #667eea; margin-bottom: 10px; }
        .article-card p { color: #666; line-height: 1.6; }
        .article-card a { color: #667eea; text-decoration: none; }
        .article-card a:hover { text-decoration: underline; }
    </style>
'''

def fix_archive_page(html_path):
    """修复单个归档页"""
    if not html_path.exists():
        return False
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题和日期
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else "技术文档"
    
    date_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', content)
    date_str = date_match.group(1) if date_match else datetime.now().strftime('%Y年%m月%d日')
    
    # 提取 hero 内容
    hero_h1_match = re.search(r'<h1>([^<]+)</h1>', content)
    hero_h1 = hero_h1_match.group(1) if hero_h1_match else title
    
    # 检查是否已有完整结构
    if 'class="navbar"' in content and 'website-background-8k.png' in content:
        print(f"  ⏭️ 已是完整结构: {html_path.name}")
        return True
    
    # 构建新页面
    new_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
{CSS_TEMPLATE}
</head>
<body>
    <div class="container">
{NAVBAR_HTML}
        <div class="hero">
            <h1>{hero_h1}</h1>
            <p>每日技术精选</p>
            <div class="hero-date">{date_str}</div>
            <a href="../../../index.html" class="back-link">← 返回首页</a>
        </div>
        <div class="content">
'''
    
    # 提取文章卡片
    article_pattern = re.compile(
        r'<div class="article-card">(.*?)</div>\s*</div>\s*<div class="footer">',
        re.DOTALL
    )
    
    # 提取内容部分
    content_match = re.search(r'<div class="content">(.*?)</div>\s*<div class="footer">', content, re.DOTALL)
    if content_match:
        article_content = content_match.group(1).strip()
        # 修复图片路径
        article_content = article_content.replace('src="images/', 'src="../../../images/')
        new_content += article_content
    
    new_content += '''
        </div>
        <div class="footer">
            <p>所有内容仅供参考学习 · ''' + date_str + '''</p>
        </div>
    </div>
</body>
</html>'''
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ 已修复: {html_path.name}")
    return True

def main():
    print("🔧 修复 tech 归档页...")
    
    archive_files = sorted(HISTORY_DIR.glob("**/2026*/**/*.html"))
    archive_files = [f for f in archive_files if f.name != 'index.html']
    
    print(f"找到 {len(archive_files)} 个归档页")
    
    for f in archive_files:
        fix_archive_page(f)
    
    print("\n✅ 全部修复完成!")

if __name__ == "__main__":
    main()