#!/bin/bash

# 归档缺失日期的技术文档

REPO_DIR="/root/.openclaw/workspace/tech-blog"
cd "$REPO_DIR"

# 归档22-24日的文档
for day in 22 23 24; do
    DATE_STR="2026年04月${day}日"
    DATE_NUM="202604${day}"
    
    echo "📝 归档 ${DATE_STR} 技术文档"
    
    # 修改归档脚本的日期
    sed -i "s/TODAY=\$(date +%Y%m%d)/TODAY=${DATE_NUM}/g" evening_archive.sh
    sed -i "s/TODAY_STR=\$(date +%Y年%m月%d日)/TODAY_STR=${DATE_STR}/g" evening_archive.sh
    
    # 运行归档脚本
    /root/.openclaw/workspace/tech-blog/evening_archive.sh
    
    # 恢复原脚本
    sed -i "s/TODAY=${DATE_NUM}/TODAY=\$(date +%Y%m%d)/g" evening_archive.sh
    sed -i "s/TODAY_STR=${DATE_STR}/TODAY_STR=\$(date +%Y年%m月%d日)/g" evening_archive.sh
    
    echo "✅ ${DATE_STR} 文档归档完成"
    echo ""
    
    # 等待1秒，避免太快
    sleep 1
done

echo "✅ 所有缺失日期文档归档完成！"