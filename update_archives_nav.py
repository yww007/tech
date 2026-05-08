#!/usr/bin/env python3
"""
更新技术文档归档页面，添加导航链接
"""

import os
import glob

# 要更新的归档文件
archive_files = [
    'history/2026/05/20260507.html',
    'history/2026/05/20260508.html',
]

# 导航 HTML (添加在 footer 之前)
nav_html = '''
        <div style="background: #f8f9fa; padding: 20px; margin: 30px 0; border-radius: 12px; text-align: center; border: 1px solid #dee2e6;">
            <p style="color: #666; margin-bottom: 10px;">
                📁 此页面为归档页面
            </p>
            <p style="margin: 0;">
                <a href="../index.html" style="color: #667eea; text-decoration: none; font-weight: 500; margin: 0 10px;">
                    ← 返回首页
                </a>
                <a href="index.html" style="color: #667eea; text-decoration: none; font-weight: 500; margin: 0 10px;">
                    📅 归档目录
                </a>
            </p>
        </div>
'''

for filepath in archive_files:
    if not os.path.exists(filepath):
        print(f"⚠️ 跳过不存在的文件: {filepath}")
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 检查是否已有导航
    if '返回首页' in content:
        print(f"✅ {filepath} 已有导航，跳过")
        continue
    
    # 在 footer 前插入导航
    new_content = content.replace('<div class="footer">', nav_html + '\n        <div class="footer">')
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f"✅ 已更新: {filepath}")

print("\n完成！")