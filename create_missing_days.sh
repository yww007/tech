#!/bin/bash

# 创建缺失日期的技术文档

REPO_DIR="/root/.openclaw/workspace/tech-blog"
cd "$REPO_DIR"

# 技术文档主题列表
declare -a topics=(
    "React组件设计模式与最佳实践"
    "数据库性能优化策略"
    "容器化部署与DevOps实践"
)

# 创建22-24日的文档
for day in 22 23 24; do
    DATE_STR="2026年04月${day}日"
    DATE_NUM="202604${day}"
    
    echo "📝 创建 ${DATE_STR} 技术文档"
    
    # 选择主题
    topic_index=$((day - 22))
    topic="${topics[$topic_index]}"
    
    # 运行自动更新脚本，但修改日期
    sed -i "s/TODAY=\$(date +%Y%m%d)/TODAY=${DATE_NUM}/g" auto_update.sh
    sed -i "s/TODAY_STR=\$(date +%Y年%m月%d日)/TODAY_STR=${DATE_STR}/g" auto_update.sh
    
    # 运行更新脚本
    /root/.openclaw/workspace/tech-blog/auto_update.sh
    
    # 恢复原脚本
    sed -i "s/TODAY=${DATE_NUM}/TODAY=\$(date +%Y%m%d)/g" auto_update.sh
    sed -i "s/TODAY_STR=${DATE_STR}/TODAY_STR=\$(date +%Y年%m月%d日)/g" auto_update.sh
    
    # 运行归档脚本
    sed -i "s/TODAY=\$(date +%Y%m%d)/TODAY=${DATE_NUM}/g" evening_archive.sh
    sed -i "s/TODAY_STR=\$(date +%Y年%m月%d日)/TODAY_STR=${DATE_STR}/g" evening_archive.sh
    
    /root/.openclaw/workspace/tech-blog/evening_archive.sh
    
    # 恢复原脚本
    sed -i "s/TODAY=${DATE_NUM}/TODAY=\$(date +%Y%m%d)/g" evening_archive.sh
    sed -i "s/TODAY_STR=${DATE_STR}/TODAY_STR=\$(date +%Y年%m月%d日)/g" evening_archive.sh
    
    echo "✅ ${DATE_STR} 文档创建完成"
    echo ""
    
    # 等待1秒，避免太快
    sleep 1
done

echo "✅ 所有缺失日期文档创建完成！"