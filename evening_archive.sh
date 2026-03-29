#!/bin/bash

# 技术文档自动归档脚本
# 北京时间每天11点运行

set -e

# 配置
REPO_DIR="/home/swg/.openclaw/workspace/tech-blog"
TODAY=$(date +%Y%m%d)
TODAY_STR=$(date +%Y年%m月%d日)
YEAR=$(date +%Y)
MONTH=$(date +%m)

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
try:
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
except:
    print(f"❌ 错误：无法读取 {index_path}")
    exit(1)

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

    # 找到最后一个 </a> 标签
    last_a_pos = content.rfind('</a>')
    if last_a_pos != -1:
        # 在最后一个 </a> 后面插入新项
        new_content = content[:last_a_pos + len('</a>')] + new_item + content[last_a_pos + len('</a>'):]
        
        # 写回
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 月份索引已更新：添加 {today_date_str} 链接")
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
    month_pattern = rf'<a href="{month}/index\.html" class="month-card">\s*<h3>{month}月 <span class="count">(\d+)天</span></h3>\s*<p>(.*?)</p>\s*</a>'
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
            <h3>{month}月 <span class="count">{day_count}天</span></h3>
            <p>{new_range}</p>
        </a>'''
        
        content = re.sub(month_pattern, new_month_card, content)
        
        # 写回
        with open(year_index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 年份索引已更新：{month}月 {day_count}天 ({new_range})")
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
