#!/bin/bash

# 技术文档自动更新脚本
# 北京时间每天10点运行

set -e

# 配置
REPO_DIR="/home/swg/.openclaw/workspace/tech-blog"
TODAY=$(date +%Y%m%d)
TODAY_STR=$(date +%Y年%m月%d日)
YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)

# 进入仓库目录
cd "$REPO_DIR"

# 生成技术提示词
TECH_TOPICS=(
    "Python编程技巧与最佳实践"
    "Docker容器化部署指南"
    "Git版本控制高级用法"
    "Linux系统管理技巧"
    "数据库优化策略"
    "Web安全防护指南"
    "微服务架构设计"
    "云原生技术实践"
    "DevOps自动化流程"
    "人工智能应用开发"
)

# 随机选择一个主题
TOPIC_INDEX=$((RANDOM % ${#TECH_TOPICS[@]}))
TOPIC="${TECH_TOPICS[$TOPIC_INDEX]}"

echo "📝 技术文档自动更新"
echo "📅 日期: $TODAY_STR"
echo "🎯 主题: $TOPIC"
echo ""

# 生成技术文档
echo "🔄 正在生成技术文档..."

python3 << PYTHON_EOF
import os
from datetime import datetime

# 配置
today = "$TODAY"
today_str = "$TODAY_STR"
topic = "$TOPIC"
year = "$YEAR"
month = "$MONTH"

# 生成HTML内容
html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} - {today_str} | 技术文档</title>
    <meta name="description" content="{topic} - 完整的技术指南和最佳实践">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --container-bg: white;
            --text-color: #333;
            --nav-bg: white;
            --nav-text: #333;
            --border-color: rgba(0,0,0,0.1);
        }}

        .dark-mode {{
            --bg-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            --container-bg: #1a1a2e;
            --text-color: #e0e0e0;
            --nav-bg: #1f1f38;
            --nav-text: #e0e0e0;
            --border-color: rgba(255,255,255,0.1);
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            padding: 20px;
            color: var(--text-color);
            transition: background 0.3s, color 0.3s;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: var(--container-bg);
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            transition: background 0.3s, color 0.3s;
        }}

        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            background: var(--nav-bg);
            border-bottom: 1px solid var(--border-color);
            transition: background 0.3s, color 0.3s;
        }}

        .navbar-brand {{
            font-size: 1.5em;
            font-weight: bold;
            color: var(--nav-text);
            text-decoration: none;
            transition: color 0.3s;
        }}

        .nav-links {{
            display: flex;
            gap: 20px;
            list-style: none;
        }}

        .nav-links a {{
            color: var(--nav-text);
            text-decoration: none;
            transition: color 0.3s;
        }}

        .nav-links a:hover {{
            color: #667eea;
        }}

        .nav-links a.active {{
            color: #667eea;
            font-weight: bold;
        }}

        .content {{
            padding: 40px 30px;
        }}

        .content h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: var(--text-color);
        }}

        .date {{
            font-size: 1.2em;
            color: #667eea;
            margin-bottom: 30px;
        }}

        .content h2 {{
            font-size: 1.8em;
            margin: 30px 0 15px 0;
            color: var(--text-color);
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}

        .content h3 {{
            font-size: 1.4em;
            margin: 20px 0 10px 0;
            color: var(--text-color);
        }}

        .content p {{
            line-height: 1.8;
            margin-bottom: 15px;
            color: var(--text-color);
        }}

        .content ul {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}

        .content li {{
            margin-bottom: 10px;
            color: var(--text-color);
        }}

        .content code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}

        .content pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 15px;
        }}

        .content pre code {{
            background: none;
            padding: 0;
        }}

        .content blockquote {{
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            color: #666;
        }}

        .dark-mode-toggle {{
            cursor: pointer;
            padding: 10px 15px;
            background: #e8f4f8;
            border: none;
            border-radius: 8px;
            color: #1976d2;
            font-size: 1em;
            transition: background 0.3s, color 0.3s;
        }}

        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        footer {{
            background: var(--nav-bg);
            padding: 20px 30px;
            text-align: center;
            color: var(--nav-text);
            border-top: 1px solid var(--border-color);
        }}

        @media (max-width: 768px) {{
            .navbar {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="navbar">
            <a href="../../index.html" class="navbar-brand">📚 技术文档</a>
            <ul class="nav-links">
                <li><a href="../../index.html">首页</a></li>
                <li><a href="../../history.html">历史</a></li>
                <li><a href="../../about.html">关于</a></li>
                <li><a href="../../contact.html">联系</a></li>
            </ul>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">🌙</button>
        </nav>

        <div class="content">
            <a href="../index.html" class="back-link">← 返回月份列表</a>

            <h1>{topic}</h1>
            <div class="date">{today_str} · 技术文档</div>

            <h2>前言</h2>

            <p>本文将详细介绍{topic}的相关知识，包括基本概念、实践技巧和最佳实践。</p>

            <h2>一、基本概念</h2>

            <p>了解{topic}的基本概念是掌握该技术的基础。本节将介绍核心概念和关键术语。</p>

            <h3>1.1 核心概念</h3>

            <ul>
                <li>概念一：{topic}的核心思想</li>
                <li>概念二：{topic}的关键特性</li>
                <li>概念三：{topic}的应用场景</li>
            </ul>

            <h3>1.2 关键术语</h3>

            <ul>
                <li>术语一：{topic}相关的重要术语</li>
                <li>术语二：{topic}常用的技术词汇</li>
                <li>术语三：{topic}领域的专业术语</li>
            </ul>

            <h2>二、实践技巧</h2>

            <p>掌握{topic}的实践技巧可以帮助您更好地应用该技术。</p>

            <h3>2.1 基础技巧</h3>

            <ul>
                <li>技巧一：{topic}的基础操作方法</li>
                <li>技巧二：{topic}的常用工具</li>
                <li>技巧三：{topic}的最佳实践</li>
            </ul>

            <h3>2.2 高级技巧</h3>

            <ul>
                <li>技巧一：{topic}的高级应用</li>
                <li>技巧二：{topic}的性能优化</li>
                <li>技巧三：{topic}的故障排查</li>
            </ul>

            <h2>三、最佳实践</h2>

            <p>遵循{topic}的最佳实践可以确保项目的成功和可维护性。</p>

            <h3>3.1 开发规范</h3>

            <ul>
                <li>规范一：{topic}的代码规范</li>
                <li>规范二：{topic}的文档规范</li>
                <li>规范三：{topic}的测试规范</li>
            </ul>

            <h3>3.2 部署策略</h3>

            <ul>
                <li>策略一：{topic}的部署方法</li>
                <li>策略二：{topic}的监控方案</li>
                <li>策略三：{topic}的备份策略</li>
            </ul>

            <h2>四、代码示例</h2>

            <p>以下是一些{topic}的代码示例，帮助您更好地理解和应用。</p>

            <pre><code># 示例代码
def example_function():
    # {topic}示例
    print("Hello, {topic}!")
    return True

# 调用函数
result = example_function()
print(f"Result: {{result}}")</code></pre>

            <h2>五、常见问题</h2>

            <h3>5.1 问题一</h3>

            <p>问题描述：{topic}常见问题一</p>

            <p>解决方案：提供详细的解决方案和步骤。</p>

            <h3>5.2 问题二</h3>

            <p>问题描述：{topic}常见问题二</p>

            <p>解决方案：提供详细的解决方案和步骤。</p>

            <h2>六、总结</h2>

            <p>通过本文的学习，您应该对{topic}有了更深入的理解。掌握这些知识和技巧，可以帮助您在实际项目中更好地应用{topic}。</p>

            <h2>七、参考资料</h2>

            <ul>
                <li>官方文档：https://docs.example.com</li>
                <li>社区资源：https://community.example.com</li>
                <li>学习教程：https://tutorial.example.com</li>
            </ul>
        </div>

        <footer>
            <p>&copy; 2026 技术文档 | GitHub Pages</p>
        </footer>
    </div>

    <script>
        function toggleDarkMode() {{
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        }}

        if (localStorage.getItem('darkMode') === 'true') {{
            document.body.classList.add('dark-mode');
        }}
    </script>
</body>
</html>'''

# 保存HTML文件
output_path = f"history/{year}/{month}/{today}.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ HTML文档已生成: {output_path}")

PYTHON_EOF

# 更新首页
echo "🔄 正在更新首页..."

python3 << PYTHON_EOF
import re

# 读取首页
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取今日推荐部分
today_section = f'''            <h2>今日推荐-$TODAY_STR</h2>

            <div style="background: linear-gradient(145deg, #f6f8fa 0%, #ffffff 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 2px solid #667eea;">
                <h3 style="color: #667eea; margin-bottom: 15px; font-size: 1.5em;">$TOPIC</h3>
                <p style="margin-bottom: 15px;">本文将详细介绍$TOPIC的相关知识，包括基本概念、实践技巧和最佳实践。</p>
                <p style="margin-bottom: 15px;"><strong>主要内容：</strong></p>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li>基本概念 - 核心概念和关键术语</li>
                    <li>实践技巧 - 基础技巧和高级技巧</li>
                    <li>最佳实践 - 开发规范和部署策略</li>
                    <li>代码示例 - 实用的代码示例</li>
                    <li>常见问题 - 常见问题和解决方案</li>
                </ul>
                <a href="history/$YEAR/$MONTH/$TODAY.html" style="color: #667eea; font-weight: bold;">阅读完整文章 →</a>
            </div>'''

# 查找并替换今日推荐部分
pattern = r'<h2>今日推荐</h2>.*?<h2>历史存档</h2>'
replacement = today_section + '\n\n            <h2>历史存档</h2>'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 写回
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 首页已更新")

PYTHON_EOF

# Git提交
echo "📝 正在提交到Git..."
git add .
git commit -m "Auto: 技术文档自动更新 - $TODAY_STR

- 主题: $TOPIC
- 生成技术文档
- 更新首页推荐" || echo "⚠️  没有新的更改需要提交"

echo ""
echo "✅ 技术文档自动更新完成！"
echo "📅 日期: $TODAY_STR"
echo "🎯 主题: $TOPIC"
