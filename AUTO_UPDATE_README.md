# 技术文档自动更新和归档

## 定时任务

### 新闻博客（yww001）

- **北京时间早上7点（UTC 23:00）** - 自动更新新闻
- **北京时间早上8点（UTC 0:00）** - 自动归档

### 技术文档（yww007）

- **北京时间早上10点（UTC 2:00）** - 自动更新技术文档
- **北京时间早上11点（UTC 3:00）** - 自动归档

## 脚本说明

### auto_update.sh

技术文档自动更新脚本，每天北京时间10点运行。

**功能：**
1. 随机选择技术主题
2. 生成技术文档配图
3. 生成HTML文档
4. 更新首页推荐
5. Git提交推送

**技术主题列表：**
- Python编程技巧与最佳实践
- Docker容器化部署指南
- Git版本控制高级用法
- Linux系统管理技巧
- 数据库优化策略
- Web安全防护指南
- 微服务架构设计
- 云原生技术实践
- DevOps自动化流程
- 人工智能应用开发

### evening_archive.sh

技术文档自动归档脚本，每天北京时间11点运行。

**功能：**
1. 检查今日文档是否存在
2. 更新月份索引
3. 更新年份索引
4. Git提交推送

## 手动运行

### 测试自动更新

```bash
cd /home/swg/.openclaw/workspace/tech-blog
./auto_update.sh
```

### 测试自动归档

```bash
cd /home/swg/.openclaw/workspace/tech-blog
./evening_archive.sh
```

## 查看定时任务

```bash
crontab -l
```

## 编辑定时任务

```bash
crontab -e
```

## 注意事项

1. **时区**：所有时间都是UTC时间，北京时间 = UTC + 8
2. **权限**：确保脚本有执行权限
3. **Git配置**：确保Git已正确配置SSH密钥
4. **API密钥**：确保NVIDIA_API_KEY已正确配置

## 故障排查

### 脚本无法运行

检查脚本权限：
```bash
chmod +x auto_update.sh evening_archive.sh
```

### Git推送失败

检查SSH密钥配置：
```bash
ssh -i /home/swg/.openclaw/workspace/github_yww007_id_ed25519 -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -T git@github.com
```

### 图片生成失败

检查NVIDIA API密钥：
```bash
cat /home/swg/.openclaw/workspace/skills/nvidia-genai/.env
```

## 更新日志

- 2026-03-29: 创建技术文档自动更新和归档脚本
- 2026-03-29: 设置定时任务
