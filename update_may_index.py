#!/usr/bin/env python3
import re

# 读取月份索引
with open('history/2026/05/index.html', 'r') as f:
    content = f.read()

# May 6 的条目
may6_entry = '''        <a href="20260506.html" class="day-card">
            <h3>2026年05月06日 <span class="count">1篇</span></h3>
            <p>Web安全防护指南 - 2026年05月06日</p>
        </a>
'''

# 检查是否已存在
if '20260506.html' in content:
    print("✅ May 6 已存在于索引中")
else:
    # 找到 May 5 的位置，在其后插入 May 6
    pattern = r'(<a href="20260505\.html" class="day-card">.*?</a>\s*)'
    replacement = r'\1\n        ' + may6_entry.strip() + '\n        '
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open('history/2026/05/index.html', 'w') as f:
        f.write(new_content)
    print("✅ 已添加 May 6 到月份索引")

print("完成！")