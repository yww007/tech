#!/bin/bash

# 技术文档自动归档脚本
# 北京时间每天11点运行

set -e

# 配置
REPO_DIR="/root/.openclaw/workspace/tech-blog"
TODAY=$(date +%Y%m%d)
TODAY_STR=$(date +%Y年%m月%d日)
YEAR=$(date +%Y)
MONTH=$(date +%m)
MONTH_DISPLAY=$(date +%-m)  # 去掉前导零（04 -> 4）

# 进入仓库目录
cd "$REPO_DIR"

echo "📝 技术文档自动归档"
echo "📅 日期: $TODAY_STR"
echo ""

# 检查今日文档是否存在
if [ ! -f "history/$YEAR/$MONTH/$TODAY.html" ]; then
    echo "⚠️  警告：今日文档不存在，跳过归档"
    exit 0
fi

# 更新月份索引
echo "🔄 正在更新月份索引..."

python3 << PYTHON_EOF
import re

# 从bash获取变量
today_file = "$TODAY"
today_date_str = "$TODAY_STR"
year = "$YEAR"
month = "$MONTH"

# 读取月份索引文件
index_path = f'history/{year}/{month}/index.html'

# 检查文件是否存在，如果不存在则创建
try:
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    # 创建新的月份索引文件
    content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{year}年{month}月 - 技术文档</title>
    <link rel="stylesheet" href="../../styles.css">
    <style>
        .month-header {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-bottom: 30px;
        }}

        .month-header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .month-header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .month-nav {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .month-nav a {{
            padding: 10px 20px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            text-decoration: none;
            color: #333;
            transition: all 0.3s;
        }}

        .month-nav a:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}

        .days-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .day-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            text-decoration: none;
            color: inherit;
        }}

        .day-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}

        .day-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.3em;
        }}

        .day-card p {{
            color: #666;
            font-size: 0.9em;
            margin: 0;
        }}

        .day-card .count {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="../../../index.html">首页</a>
            <a href="../index.html">{year}年</a>
            <a href="index.html" class="active">{month}月</a>
        </nav>
    </header>

    <div class="month-header">
        <h1>📅 {year}年{month}月</h1>
        <p>技术文档</p>
    </div>

    <div class="month-nav">
        <a href="../index.html">← 返回年份列表</a>
        <a href="../../../index.html">返回首页</a>
    </div>

    <div class="days-grid">
    </div>

    <footer>
        <p>&copy; {year} 技术文档 | GitHub Pages</p>
    </footer>
</body>
</html>'''
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已创建新的月份索引文件：{index_path}")

# 提取今日文档标题（用于索引描述）
try:
    with open(f'history/{year}/{month}/{today_file}.html', 'r', encoding='utf-8') as f:
        doc_html = f.read()
    
    # 提取标题
    import re
    title_match = re.search(r'<h1>(.*?)</h1>', doc_html)
    if title_match:
        title = title_match.group(1).strip()
        # 取前30个字符
        if len(title) > 30:
            title = title[:30] + '...'
    else:
        title = "技术文档"
    
except:
    title = "技术文档"

# 检查是否已包含今日的链接
if today_file not in content:
    # 生成新的历史项
    new_item = f'''
        <a href="{today_file}.html" class="day-card">
            <h3>{today_date_str} <span class="count">1篇</span></h3>
            <p>{title}</p>
        </a>'''

    # 找到days-grid里面的最后一个 </a> 标签
    days_grid_start = content.find('<div class="days-grid">')
    if days_grid_start != -1:
        days_grid_end = content.find('</div>', days_grid_start + len('<div class="days-grid">'))
        if days_grid_end != -1:
            # 在days-grid里面找最后一个 </a> 标签
            days_grid_content = content[days_grid_start:days_grid_end]
            last_a_pos = days_grid_content.rfind('</a>')
            if last_a_pos != -1:
                # 在days-grid里面的最后一个 </a> 后面插入新项
                insert_pos = days_grid_start + last_a_pos + len('</a>')
                new_content = content[:insert_pos] + new_item + content[insert_pos:]
                
                # 写回
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ 月份索引已更新：添加 {today_date_str} 链接")
            else:
                # days-grid里面没有</a>标签，直接插入
                insert_pos = days_grid_start + len('<div class="days-grid">')
                new_content = content[:insert_pos] + new_item + content[insert_pos:]
                
                # 写回
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ 月份索引已更新：添加 {today_date_str} 链接")
        else:
            print(f"❌ 错误：无法找到days-grid的结束标签")
    else:
        print(f"❌ 错误：无法找到days-grid")
else:
    print(f"⏭️  月份索引已包含 {today_date_str}，跳过更新")

PYTHON_EOF

echo ""

# 更新年份索引
echo "🔄 正在更新年份索引..."

python3 << PYTHON_EOF
import re

# 从bash获取变量
year = "$YEAR"
month = "$MONTH"
month_display = "$MONTH_DISPLAY"

# 读取年份索引文件
year_index_path = f'history/{year}/index.html'
try:
    with open(year_index_path, 'r', encoding='utf-8') as f:
        content = f.read()
except:
    print(f"❌ 错误：无法读取 {year_index_path}")
    exit(1)

# 计算当前月份有多少天
month_index_path = f'history/{year}/{month}/index.html'
try:
    with open(month_index_path, 'r', encoding='utf-8') as f:
        month_content = f.read()
    
    # 统计 day-card 的数量
    day_count = month_content.count('class="day-card"')
    
    # 更新月份卡片的天数和日期范围
    month_pattern = rf'<a href="{month}/index\.html" class="month-card">\s*<h3>{month_display}月 <span class="count">(\d+)天</span></h3>\s*<p>(.*?)</p>\s*</a>'
    match = re.search(month_pattern, content)
    
    if match:
        old_count = match.group(1)
        old_range = match.group(2)
        
        # 提取日期范围（如 "3月22日 - 3月28日"）
        if ' - ' in old_range:
            start_date = old_range.split(' - ')[0]
            # 更新结束日期为当前日期
            today_str = "$TODAY_STR"
            new_range = f"{start_date} - {today_str}"
        else:
            new_range = old_range
        
        # 替换
        new_month_card = f'''<a href="{month}/index.html" class="month-card">
            <h3>{month_display}月 <span class="count">{day_count}天</span></h3>
            <p>{new_range}</p>
        </a>'''
        
        content = re.sub(month_pattern, new_month_card, content)
        
        # 写回
        with open(year_index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 年份索引已更新：{month}月 {day_count}天 ({new_range})")
    else:
        # 不存在链接卡片，检查是否存在disabled卡片
        disabled_pattern = rf'<div class="month-card disabled">\s*<h3>{month_display}月</h3>\s*<p>暂无数据</p>\s*</div>'
        disabled_match = re.search(disabled_pattern, content)
        
        if disabled_match:
            # 将disabled卡片替换为链接卡片
            today_str = "$TODAY_STR"
            new_month_card = f'''<a href="{month}/index.html" class="month-card">
            <h3>{month_display}月 <span class="count">{day_count}天</span></h3>
            <p>{today_str}</p>
        </a>'''
            
            content = re.sub(disabled_pattern, new_month_card, content)
            
            # 写回
            with open(year_index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 年份索引已更新：{month}月 {day_count}天 ({today_str})")
        else:
            print(f"⚠️  警告：无法找到 {month}月的卡片")
        
except Exception as e:
    print(f"❌ 错误：无法更新年份索引 - {e}")

PYTHON_EOF

echo ""

# Git提交推送
echo "📝 正在提交到Git..."
git add history/$YEAR/$MONTH/$TODAY.html history/$YEAR/$MONTH/index.html history/$YEAR/index.html index.html
git commit -m "Auto: 技术文档自动归档 - $TODAY_STR

- 拷贝历史模板并替换日期
- 从首页提取文档内容
- 更新月份索引页面
- 更新年份索引页面" || echo "⚠️  没有新的更改需要提交"

git push

echo ""
echo "✅ 技术文档自动归档完成！"
echo "📅 日期: $TODAY_STR"
