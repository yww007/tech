#!/usr/bin/env python3
"""
技术文档自动更新脚本
包含图片生成功能
参考环球新闻的图片生成逻辑
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import time

# 配置
BLOG_PATH = "/home/swg/.openclaw/workspace/tech-blog"
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")
IMAGES_DIR = Path(BLOG_PATH) / "images"
LOGS_DIR = Path(BLOG_PATH) / "logs"

# 创建必要的目录
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class Logger:
    def __init__(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = LOGS_DIR / f"{today}.log"
        self.log("=" * 60)
        self.log(f"开始更新技术文档 - {datetime.now()}")
        self.log("=" * 60)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")

logger = Logger()

def get_beijing_time():
    """获取北京时间（UTC+8）"""
    return datetime.now() + timedelta(hours=8)

def get_tech_topic():
    """获取技术主题（按日期轮换，避免重复）"""
    TECH_TOPICS = [
        "Python编程技巧与最佳实践",
        "Docker容器化部署指南",
        "Git版本控制高级用法",
        "Linux系统管理技巧",
        "数据库优化策略",
        "Web安全防护指南",
        "微服务架构设计",
        "云原生技术实践",
        "DevOps自动化流程",
        "人工智能应用开发"
    ]

    # 按日期轮换，避免重复
    day_of_year = datetime.now().timetuple().tm_yday
    topic_index = (day_of_year - 1) % len(TECH_TOPICS)
    return TECH_TOPICS[topic_index]

def get_topic_content(topic):
    """获取主题的具体内容"""
    content_map = {
        "Python编程技巧与最佳实践": {
            "intro": "Python是一门简洁而强大的编程语言，掌握其编程技巧和最佳实践可以显著提升代码质量和开发效率。本文将介绍Python的高级特性、性能优化技巧、代码规范以及常见陷阱的避免方法。",
            "concepts": {
                "核心概念": [
                    "列表推导式 - 一行代码生成列表，简洁高效",
                    "生成器 - 惰性求值，节省内存",
                    "装饰器 - 函数包装器，增强功能",
                    "上下文管理器 - 自动资源管理，with语句"
                ],
                "关键术语": [
                    "PEP 8 - Python官方代码风格指南",
                    "GIL - 全局解释器锁，影响多线程性能",
                    "鸭子类型 - 不关注类型，关注行为",
                    "魔法方法 - 以__开头和结尾的特殊方法"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用f-string格式化字符串，比%和.format()更快更易读",
                    "善用enumerate()同时获取索引和值",
                    "使用zip()并行遍历多个序列",
                    "用collections.Counter统计元素出现次数"
                ],
                "高级技巧": [
                    "使用@lru_cache缓存函数结果，避免重复计算",
                    "用__slots__减少内存占用，适合大量实例",
                    "使用asyncio实现异步编程，提升IO密集型任务性能",
                    "用multiprocessing绕过GIL限制，实现真正的并行"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "遵循PEP 8规范，使用black自动格式化",
                    "编写docstring文档，使用Google或NumPy风格",
                    "使用类型注解，提高代码可读性和IDE支持",
                    "编写单元测试，使用pytest框架"
                ],
                "部署策略": [
                    "使用虚拟环境隔离依赖，推荐venv或conda",
                    "用requirements.txt或pyproject.toml管理依赖",
                    "使用Docker容器化部署，保证环境一致性",
                    "配置CI/CD流水线，自动化测试和部署"
                ]
            },
            "code_example": '''# Python最佳实践示例

from functools import lru_cache
from typing import List, Optional
from dataclasses import dataclass
from contextlib import contextmanager

# 1. 使用类型注解和dataclass
@dataclass
class User:
    id: int
    name: str
    email: Optional[str] = None

# 2. 使用装饰器缓存结果
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """计算斐波那契数列（带缓存）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 3. 使用上下文管理器
@contextmanager
def timer(name: str):
    """计时上下文管理器"""
    import time
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"{name} 耗时: {elapsed:.3f}秒")

# 4. 使用列表推导式和生成器
def process_users(users: List[User]) -> List[str]:
    """处理用户列表"""
    # 列表推导式
    active_users = [u for u in users if u.email]
    # 生成器表达式
    emails = (u.email for u in active_users if u.email)
    return list(emails)

# 使用示例
if __name__ == "__main__":
    with timer("斐波那契计算"):
        result = fibonacci(35)
        print(f"fibonacci(35) = {result}")

    users = [
        User(1, "Alice", "alice@example.com"),
        User(2, "Bob", "bob@example.com"),
        User(3, "Charlie", None)
    ]

    emails = process_users(users)
    print(f"活跃用户邮箱: {emails}")''',
            "faq": [
                {
                    "question": "如何提升Python代码性能？",
                    "answer": "1. 使用内置函数和库（如sum()、map()）比循环更快；2. 使用生成器代替列表，节省内存；3. 使用@lru_cache缓存重复计算；4. 对于CPU密集型任务，使用multiprocessing；5. 使用C扩展（如NumPy、Cython）加速数值计算。"
                },
                {
                    "question": "Python多线程为什么不能提升性能？",
                    "answer": "因为Python有GIL（全局解释器锁），同一时刻只能有一个线程执行Python字节码。多线程适合IO密集型任务（如网络请求、文件读写），对于CPU密集型任务，应该使用multiprocessing实现真正的并行。"
                }
            ],
            "references": [
                "官方文档：https://docs.python.org/zh-cn/3/",
                "PEP 8风格指南：https://peps.python.org/pep-0008/",
                "Real Python教程：https://realpython.com/"
            ]
        },
        "Docker容器化部署指南": {
            "intro": "Docker通过容器化技术实现了应用的轻量级虚拟化，让应用在任何环境中都能一致运行。本文将详细介绍Docker的核心概念、镜像构建、容器管理、网络配置以及生产环境部署的最佳实践。",
            "concepts": {
                "核心概念": [
                    "镜像 - 只读的应用模板，包含运行所需的一切",
                    "容器 - 镜像的运行实例，相互隔离",
                    "Dockerfile - 构建镜像的脚本文件",
                    "Docker Compose - 多容器编排工具"
                ],
                "关键术语": [
                    "Layer - 镜像的分层结构，共享基础层",
                    "Volume - 数据卷，持久化存储",
                    "Network - 容器网络，容器间通信",
                    "Registry - 镜像仓库，如Docker Hub"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用多阶段构建减小镜像体积",
                    "在.dockerignore中排除不必要的文件",
                    "使用非root用户运行容器，提升安全性",
                    "使用健康检查确保容器正常运行"
                ],
                "高级技巧": [
                    "使用Docker Compose编排多容器应用",
                    "配置自定义网络实现容器间通信",
                    "使用Volume实现数据持久化和共享",
                    "使用Secret和Config管理敏感信息"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "每个容器只运行一个进程，保持简单",
                    "使用官方基础镜像，定期更新安全补丁",
                    "镜像标签使用语义化版本，避免使用latest",
                    "编写详细的Dockerfile注释，便于维护"
                ],
                "部署策略": [
                    "使用CI/CD自动构建和推送镜像",
                    "配置资源限制（CPU、内存），防止资源耗尽",
                    "使用日志驱动收集容器日志",
                    "配置自动重启策略，保证服务可用性"
                ]
            },
            "code_example": '''# Dockerfile最佳实践示例

# 多阶段构建示例
# 第一阶段：构建
FROM python:3.11-slim AS builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖到临时目录
RUN pip install --user --no-cache-dir -r requirements.txt

# 第二阶段：运行
FROM python:3.11-slim

WORKDIR /app

# 从构建阶段复制依赖
COPY --from=builder /root/.local /root/.local

# 确保PATH包含用户安装的包
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \\
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

---
# docker-compose.yml示例
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge''',
            "faq": [
                {
                    "question": "如何减小Docker镜像体积？",
                    "answer": "1. 使用alpine等轻量级基础镜像；2. 多阶段构建，只保留运行时需要的文件；3. 在RUN命令后清理缓存（apt-get clean）；4. 使用.dockerignore排除不必要的文件；5. 合并RUN命令减少层数。"
                },
                {
                    "question": "容器内数据会丢失吗？",
                    "answer": "是的，容器删除后数据会丢失。解决方案：1. 使用Volume或Bind Mount挂载宿主机目录；2. 使用数据卷容器；3. 对于数据库等重要数据，定期备份到宿主机或云存储。"
                }
            ],
            "references": [
                "Docker官方文档：https://docs.docker.com/",
                "Docker Hub：https://hub.docker.com/",
                "Docker Compose文档：https://docs.docker.com/compose/"
            ]
        },
        "Git版本控制高级用法": {
            "intro": "Git是现代软件开发不可或缺的版本控制工具。掌握Git的高级用法可以让你更高效地管理代码、协作开发、处理冲突和回滚错误。本文将介绍Git的高级命令、工作流、分支策略和最佳实践。",
            "concepts": {
                "核心概念": [
                    "HEAD - 指向当前分支的最新提交",
                    "Index/Stage - 暂存区，准备提交的文件",
                    "Reflog - 引用日志，记录所有HEAD移动",
                    "Rebase - 变基，重写提交历史"
                ],
                "关键术语": [
                    "Fast-forward - 快进合并，无分叉",
                    "Merge commit - 合并提交，保留历史",
                    "Squash - 压缩提交，合并多个提交",
                    "Cherry-pick - 挑选提交，应用到其他分支"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用git stash临时保存工作区修改",
                    "用git reflog找回误删的提交",
                    "使用git bisect二分查找引入bug的提交",
                    "用git blame查看每行代码的修改历史"
                ],
                "高级技巧": [
                    "使用git rebase -i交互式变基，整理提交历史",
                    "用git cherry-pick将特定提交应用到其他分支",
                    "使用git worktree同时检出多个分支",
                    "配置git hooks实现自动化检查和部署"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "提交信息使用约定式提交（Conventional Commits）",
                    "保持提交原子性，一次提交只做一件事",
                    "定期推送远程分支，避免丢失本地提交",
                    "使用.gitignore忽略不必要的文件"
                ],
                "部署策略": [
                    "使用Git Flow或GitHub Flow分支策略",
                    "保护主分支，要求代码审查和CI通过",
                    "使用标签（tag）标记版本发布",
                    "配置CI/CD自动测试和部署"
                ]
            },
            "code_example": '''# Git高级用法示例

# 1. 交互式变基 - 整理最近3个提交
git rebase -i HEAD~3

# 2. 暂存和恢复工作区
git stash push -m "临时保存功能A"
git stash list
git stash pop stash@{0}

# 3. 挑选特定提交到当前分支
git cherry-pick <commit-hash>

# 4. 二分查找bug
git bisect start
git bisect bad HEAD
git bisect good <good-commit-hash>
# Git会自动切换到中间提交，测试后标记good或bad
git bisect reset

# 5. 查看文件历史
git log --follow --all -- filename.txt
git blame filename.txt

# 6. 撤销操作
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最后一次提交（丢弃修改）
git reset --hard HEAD~1

# 撤销已推送的提交（创建新提交）
git revert <commit-hash>

# 7. 分支管理
# 创建并切换到新分支
git checkout -b feature/new-feature

# 合并分支（创建合并提交）
git merge feature/new-feature

# 变基合并（线性历史）
git rebase main

# 8. 远程操作
# 查看远程分支
git branch -r

# 跟踪远程分支
git checkout -b local-branch origin/remote-branch

# 强制推送（谨慎使用）
git push --force-with-lease origin feature-branch

---
# .gitignore示例
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db

# 环境变量
.env
.env.local

---
# Git Hooks示例（pre-commit）
#!/bin/bash
# .git/hooks/pre-commit

# 运行代码格式检查
echo "运行代码格式检查..."
black --check .

# 运行测试
echo "运行测试..."
pytest

# 如果检查失败，阻止提交
if [ $? -ne 0 ]; then
    echo "❌ 预提交检查失败，请修复后再提交"
    exit 1
fi''',
            "faq": [
                {
                    "question": "git merge和git rebase有什么区别？",
                    "answer": "merge会创建一个合并提交，保留完整的历史记录，适合公共分支；rebase会将提交移动到目标分支顶端，产生线性的历史记录，适合个人分支整理。rebase会改变提交历史，已推送的分支不要rebase。"
                },
                {
                    "question": "如何解决合并冲突？",
                    "answer": "1. git status查看冲突文件；2. 打开文件，找到<<<<<<<和>>>>>>>标记；3. 手动编辑解决冲突；4. git add标记为已解决；5. git commit完成合并。使用git mergetool可以图形化解决冲突。"
                }
            ],
            "references": [
                "Git官方文档：https://git-scm.com/doc",
                "Pro Git书籍：https://git-scm.com/book/zh/v2",
                "GitHub Flow：https://guides.github.com/introduction/flow/"
            ]
        },
        "Linux系统管理技巧": {
            "intro": "Linux是服务器和开发环境的主流操作系统。掌握Linux系统管理技巧可以让你更高效地监控系统、排查问题、优化性能和自动化运维。本文将介绍Linux的核心命令、系统监控、性能优化和自动化脚本。",
            "concepts": {
                "核心概念": [
                    "进程 - 运行中的程序实例，有PID",
                    "文件权限 - rwx权限位，控制访问",
                    "Shell - 命令解释器，如bash、zsh",
                    "服务 - 后台运行的守护进程"
                ],
                "关键术语": [
                    "PID - 进程ID，唯一标识进程",
                    "TTY - 终端设备，进程的输入输出",
                    "Signal - 信号，进程间通信机制",
                    "Cron - 定时任务调度器"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用top/htop实时监控系统资源",
                    "用ps aux查看所有进程，配合grep过滤",
                    "使用netstat/ss查看网络连接和端口",
                    "用df -h查看磁盘使用情况，du -sh查看目录大小"
                ],
                "高级技巧": [
                    "使用strace跟踪系统调用，排查程序问题",
                    "用tcpdump抓包分析网络流量",
                    "使用journalctl查看systemd日志",
                    "配置logrotate自动轮转日志文件"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "使用sudo执行需要root权限的命令",
                    "定期更新系统和软件包，安装安全补丁",
                    "配置防火墙（ufw/iptables），限制不必要的端口",
                    "使用SSH密钥认证，禁用密码登录"
                ],
                "部署策略": [
                    "使用Ansible/Terraform自动化配置管理",
                    "配置监控告警（Prometheus+Grafana）",
                    "定期备份重要数据，测试恢复流程",
                    "使用容器化部署，保证环境一致性"
                ]
            },
            "code_example": '''# Linux系统管理实用脚本

# 1. 监控系统资源
#!/bin/bash
# monitor.sh - 系统监控脚本

echo "=== 系统资源监控 ==="
echo "时间: $(date)"
echo ""

# CPU使用率
echo "📊 CPU使用率:"
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\\([0-9.]*\\)%* id.*/\\1/" | awk '{print 100 - $1"%"}'

# 内存使用
echo ""
echo "💾 内存使用:"
free -h | awk '/Mem:/ {printf "  总计: %s\\n  已用: %s\\n  空闲: %s\\n", $2, $3, $4}'

# 磁盘使用
echo ""
echo "💿 磁盘使用:"
df -h | awk '$NF=="/"{printf "  根分区: %s / %s (%s)\\n", $3, $2, $5}'

# 负载
echo ""
echo "⚡ 系统负载:"
uptime | awk -F'load average:' '{print "  " $2}'

# 2. 查找并清理大文件
#!/bin/bash
# clean_large_files.sh - 查找大于100MB的文件

echo "查找大于100MB的文件:"
find / -type f -size +100M 2>/dev/null | head -20

# 3. 监控特定进程
#!/bin/bash
# monitor_process.sh - 监控进程

PROCESS_NAME="nginx"
if pgrep -x "$PROCESS_NAME" > /dev/null; then
    echo "✅ $PROCESS_NAME 正在运行 (PID: $(pgrep -x $PROCESS_NAME))"
else
    echo "❌ $PROCESS_NAME 未运行"
    # 尝试重启
    systemctl restart $PROCESS_NAME
fi

# 4. 日志分析
#!/bin/bash
# analyze_logs.sh - 分析Nginx访问日志

LOG_FILE="/var/log/nginx/access.log"

echo "=== 访问日志分析 ==="
echo "总请求数: $(wc -l < $LOG_FILE)"
echo "独立IP数: $(awk '{print $1}' $LOG_FILE | sort | uniq | wc -l)"
echo ""
echo "Top 10 访问IP:"
awk '{print $1}' $LOG_FILE | sort | uniq -c | sort -rn | head -10
echo ""
echo "Top 10 访问URL:"
awk '{print $7}' $LOG_FILE | sort | uniq -c | sort -rn | head -10

# 5. 自动备份脚本
#!/bin/bash
# backup.sh - 自动备份

BACKUP_DIR="/backup"
SOURCE_DIR="/var/www"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行备份
tar -czf $BACKUP_FILE $SOURCE_DIR

# 删除7天前的备份
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete

echo "✅ 备份完成: $BACKUP_FILE"

# 6. 系统安全检查
#!/bin/bash
# security_check.sh - 安全检查

echo "=== 系统安全检查 ==="

# 检查SSH配置
echo "🔒 SSH配置:"
grep -E "^(PermitRootLogin|PasswordAuthentication)" /etc/ssh/sshd_config

# 检查开放端口
echo ""
echo "🌐 开放端口:"
ss -tuln | grep LISTEN

# 检查失败登录
echo ""
echo "⚠️  最近失败登录:"
lastb | head -10

# 检查磁盘空间
echo ""
echo "💿 磁盘使用率:"
df -h | awk '$5+0 > 80 {print "警告: " $1 " 使用率 " $5}'

# 7. Cron定时任务示例
# 每天凌晨2点执行备份
0 2 * * * /root/scripts/backup.sh >> /var/log/backup.log 2>&1

# 每小时检查进程
0 * * * * /root/scripts/monitor_process.sh >> /var/log/monitor.log 2>&1

# 每周日凌晨3点清理日志
0 3 * * 0 /root/scripts/clean_logs.sh >> /var/log/clean.log 2>&1''',
            "faq": [
                {
                    "question": "如何查看Linux系统负载？",
                    "answer": "使用uptime或top命令查看负载。负载三个数字分别表示1分钟、5分钟、15分钟的平均负载。如果负载持续高于CPU核心数，说明系统负载过高。使用htop可以更直观地查看CPU、内存、进程状态。"
                },
                {
                    "question": "如何排查Linux系统性能问题？",
                    "answer": "1. 使用top/htop查看CPU和内存使用；2. 用iostat查看磁盘IO；3. 用netstat/ss查看网络连接；4. 用strace跟踪系统调用；5. 查看系统日志/var/log/；6. 使用perf进行性能分析。"
                }
            ],
            "references": [
                "Linux命令大全：https://linuxtools-rst.readthedocs.io/",
                "系统管理指南：https://access.redhat.com/documentation/",
                "Shell脚本编程：https://www.shellscript.sh/"
            ]
        },
        "数据库优化策略": {
            "intro": "数据库是应用系统的核心，其性能直接影响整个系统的响应速度和用户体验。本文将介绍数据库索引优化、查询优化、架构设计、缓存策略以及监控调优的最佳实践，帮助你构建高性能的数据库系统。",
            "concepts": {
                "核心概念": [
                    "索引 - 加速查询的数据结构",
                    "事务 - 保证数据一致性的机制",
                    "锁 - 控制并发访问的机制",
                    "分区 - 将大表拆分为多个小表"
                ],
                "关键术语": [
                    "主键 - 唯一标识记录的列",
                    "外键 - 关联其他表的列",
                    "复合索引 - 包含多个列的索引",
                    "覆盖索引 - 包含查询所需所有列的索引"
                ]
            },
            "practices": {
                "基础技巧": [
                    "为WHERE、ORDER BY、JOIN的列创建索引",
                    "避免SELECT *，只查询需要的列",
                    "使用EXPLAIN分析查询执行计划",
                    "合理使用LIMIT分页，避免深分页"
                ],
                "高级技巧": [
                    "使用读写分离，主库写、从库读",
                    "实现分库分表，水平拆分大表",
                    "使用连接池，减少连接开销",
                    "配置慢查询日志，定期分析优化"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "使用参数化查询，防止SQL注入",
                    "合理设计表结构，遵循范式化原则",
                    "使用事务保证数据一致性",
                    "定期备份数据，测试恢复流程"
                ],
                "部署策略": [
                    "配置主从复制，实现高可用",
                    "使用Redis缓存热点数据",
                    "监控数据库性能指标（QPS、慢查询）",
                    "定期优化表和索引（OPTIMIZE TABLE）"
                ]
            },
            "code_example": '''# 数据库优化SQL示例

-- 1. 索引优化
-- 为常用查询条件创建索引
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_order_status_date ON orders(status, created_at);

-- 复合索引（注意列顺序）
CREATE INDEX idx_user_status_created ON users(status, created_at);

-- 2. 查询优化
-- ❌ 不好的查询（全表扫描）
SELECT * FROM users WHERE name LIKE '%张%';

-- ✅ 好的查询（使用索引）
SELECT id, name, email FROM users WHERE name = '张三';

-- ❌ 不好的分页（深分页性能差）
SELECT * FROM orders ORDER BY id LIMIT 100000, 10;

-- ✅ 好的分页（使用游标）
SELECT * FROM orders WHERE id > 100000 ORDER BY id LIMIT 10;

-- 3. JOIN优化
-- 使用小表驱动大表
SELECT u.name, o.order_id
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- 4. 子查询优化
-- ❌ 不好的子查询
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);

-- ✅ 好的JOIN
SELECT DISTINCT u.* FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.amount > 1000;

-- 5. 事务使用
BEGIN TRANSACTION;

-- 执行多个操作
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- 提交事务
COMMIT;

-- 出错时回滚
-- ROLLBACK;

-- 6. 批量插入
-- ❌ 不好的方式（多次插入）
INSERT INTO logs (message, created_at) VALUES ('msg1', NOW());
INSERT INTO logs (message, created_at) VALUES ('msg2', NOW());

-- ✅ 好的方式（批量插入）
INSERT INTO logs (message, created_at) VALUES
    ('msg1', NOW()),
    ('msg2', NOW()),
    ('msg3', NOW());

-- 7. 分区表示例
-- 按日期范围分区
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10,2),
    status VARCHAR(20),
    created_at DATETIME
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);

-- 8. 慢查询分析
-- 启用慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;  -- 超过2秒的查询

-- 查看慢查询
SHOW VARIABLES LIKE 'slow_query%';
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- 9. 表优化
-- 优化表（重建表，消除碎片）
OPTIMIZE TABLE users;

-- 分析表（更新统计信息）
ANALYZE TABLE users;

-- 10. 监控查询
-- 查看当前执行的查询
SHOW PROCESSLIST;

-- 杀掉长时间运行的查询
KILL <process_id>;''',
            "faq": [
                {
                    "question": "什么时候应该创建索引？",
                    "answer": "1. WHERE、ORDER BY、GROUP BY、JOIN的列；2. 频繁查询但不常更新的列；3. 区分度高的列（如用户名、订单号）；4. 外键列。注意：索引会降低写入性能，不要过度索引。"
                },
                {
                    "question": "如何解决数据库死锁？",
                    "answer": "1. 使用SHOW ENGINE INNODB STATUS查看死锁信息；2. 分析死锁原因，通常是事务顺序不一致；3. 统一事务中表的访问顺序；4. 减少事务持有锁的时间；5. 使用乐观锁代替悲观锁。"
                }
            ],
            "references": [
                "MySQL官方文档：https://dev.mysql.com/doc/",
                "PostgreSQL文档：https://www.postgresql.org/docs/",
                "数据库性能优化：https://use-the-index-luke.com/"
            ]
        },
        "Web安全防护指南": {
            "intro": "Web安全是应用开发不可忽视的重要环节。一次安全漏洞可能导致数据泄露、服务中断甚至法律风险。本文将介绍常见的Web安全威胁、防护措施、安全测试和合规要求，帮助你构建安全可靠的Web应用。",
            "concepts": {
                "核心概念": [
                    "XSS - 跨站脚本攻击，注入恶意脚本",
                    "CSRF - 跨站请求伪造，伪造用户请求",
                    "SQL注入 - 注入恶意SQL语句",
                    "DDoS - 分布式拒绝服务攻击"
                ],
                "关键术语": [
                    "HTTPS - 加密传输协议",
                    "CSP - 内容安全策略",
                    "CORS - 跨域资源共享",
                    "JWT - JSON Web Token"
                ]
            },
            "practices": {
                "基础技巧": [
                    "对所有用户输入进行验证和过滤",
                    "使用参数化查询防止SQL注入",
                    "对输出进行HTML转义防止XSS",
                    "使用HTTPS加密传输"
                ],
                "高级技巧": [
                    "配置CSP限制脚本来源",
                    "使用CSRF Token防止跨站请求伪造",
                    "实现速率限制防止暴力破解",
                    "定期进行安全审计和渗透测试"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "遵循OWASP Top 10安全指南",
                    "使用安全框架和库（如Django、Spring Security）",
                    "定期更新依赖，修复安全漏洞",
                    "最小权限原则，限制用户访问"
                ],
                "部署策略": [
                    "配置WAF（Web应用防火墙）",
                    "启用安全响应头（CSP、X-Frame-Options）",
                    "配置日志监控，及时发现异常",
                    "定期备份数据，制定应急响应计划"
                ]
            },
            "code_example": '''# Web安全防护代码示例

# 1. SQL注入防护（Python）
# ❌ 不安全的代码（SQL注入）
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)

# ✅ 安全的代码（参数化查询）
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))

# 使用ORM（更安全）
user = User.objects.filter(username=username).first()

# 2. XSS防护
# ❌ 不安全的代码（XSS漏洞）
return f"<div>用户名: {username}</div>"

# ✅ 安全的代码（HTML转义）
from html import escape
return f"<div>用户名: {escape(username)}</div>"

# 使用模板引擎（自动转义）
return render_template('user.html', username=username)

# 3. CSRF防护
# Flask示例
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# 在表单中添加CSRF token
<form method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <input type="text" name="username">
    <button type="submit">提交</button>
</form>

# 4. 密码安全
# ❌ 不安全的密码存储
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ 安全的密码存储（使用bcrypt）
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# 验证密码
if bcrypt.checkpw(password.encode(), stored_hash):
    # 密码正确
    pass

# 5. JWT认证
import jwt
from datetime import datetime, timedelta

# 生成JWT
payload = {
    'user_id': user.id,
    'exp': datetime.utcnow() + timedelta(hours=24)
}
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# 验证JWT
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user_id = payload['user_id']
except jwt.ExpiredSignatureError:
    # Token过期
    pass

# 6. 文件上传安全
# 验证文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \\
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 验证文件内容（不仅看扩展名）
import magic

def is_valid_image(file):
    file_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)  # 重置文件指针
    return file_type.startswith('image/')

# 7. 安全响应头配置
# Nginx配置
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
add_header Content-Security-Policy "default-src 'self'";

# 8. 速率限制
# Flask示例
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # 登录逻辑
    pass

# 9. 输入验证
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @validator('username')
    def username_length(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('用户名长度必须在3-20之间')
        return v

    @validator('email')
    def email_format(cls, v):
        if '@' not in v:
            raise ValueError('邮箱格式不正确')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少8位')
        return v''',
            "faq": [
                {
                    "question": "如何防止SQL注入？",
                    "answer": "1. 使用参数化查询或ORM；2. 对所有用户输入进行验证和过滤；3. 使用最小权限的数据库账户；4. 避免拼接SQL语句；5. 定期进行安全审计。"
                },
                {
                    "question": "HTTPS和HTTP有什么区别？",
                    "answer": "HTTPS使用SSL/TLS加密传输，防止数据被窃听和篡改；HTTP是明文传输，不安全。HTTPS需要SSL证书，可以申请免费的Let's Encrypt证书。生产环境必须使用HTTPS。"
                }
            ],
            "references": [
                "OWASP Top 10：https://owasp.org/www-project-top-ten/",
                "Web安全测试：https://owasp.org/www-project-web-security-testing-guide/",
                "Cheat Sheet Series：https://cheatsheetseries.owasp.org/"
            ]
        },
        "微服务架构设计": {
            "intro": "微服务架构将单体应用拆分为多个小型服务，每个服务独立开发、部署和扩展。这种架构提高了系统的灵活性和可维护性，但也带来了分布式系统的复杂性。本文将介绍微服务的设计原则、通信机制、服务治理和最佳实践。",
            "concepts": {
                "核心概念": [
                    "服务拆分 - 按业务领域拆分服务",
                    "服务发现 - 动态发现服务实例",
                    "API网关 - 统一入口，路由请求",
                    "配置中心 - 集中管理配置"
                ],
                "关键术语": [
                    "RPC - 远程过程调用",
                    "REST - 表述性状态转移",
                    "gRPC - Google RPC框架",
                    "消息队列 - 异步通信"
                ]
            },
            "practices": {
                "基础技巧": [
                    "按业务边界拆分服务，避免过度拆分",
                    "使用RESTful API或gRPC进行服务间通信",
                    "实现服务注册与发现（如Consul、Eureka）",
                    "配置API网关统一管理路由"
                ],
                "高级技巧": [
                    "使用消息队列实现异步通信和解耦",
                    "实现分布式事务（Saga模式、TCC）",
                    "配置熔断器防止级联故障",
                    "实现链路追踪，快速定位问题"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "每个服务有独立的数据库（Database per Service）",
                    "服务间通信使用异步消息，避免同步调用",
                    "实现幂等性，支持重试",
                    "版本化API，保证向后兼容"
                ],
                "部署策略": [
                    "使用容器化部署（Docker+Kubernetes）",
                    "实现自动扩缩容，应对流量波动",
                    "配置蓝绿部署或金丝雀发布",
                    "集中收集日志和监控指标"
                ]
            },
            "code_example": '''# 微服务架构示例

# 1. 服务拆分示例
# 用户服务（user-service）
# 负责用户管理、认证授权
# 端口: 8001
# 数据库: user_db

# 订单服务（order-service）
# 负责订单管理、支付处理
# 端口: 8002
# 数据库: order_db

# 商品服务（product-service）
# 负责商品管理、库存控制
# 端口: 8003
# 数据库: product_db

# 2. API网关配置（Kong）
# kong.yml
_format_version: "3.0"

services:
  - name: user-service
    url: http://user-service:8001
    routes:
      - name: user-routes
        paths:
          - /api/users

  - name: order-service
    url: http://order-service:8002
    routes:
      - name: order-routes
        paths:
          - /api/orders

  - name: product-service
    url: http://product-service:8003
    routes:
      - name: product-routes
        paths:
          - /api/products

# 3. 服务发现（Consul）
# consul配置
{
  "service": {
    "name": "user-service",
    "tags": ["api"],
    "address": "192.168.1.100",
    "port": 8001,
    "check": {
      "http": "http://192.168.1.100:8001/health",
      "interval": "10s"
    }
  }
}

# 4. gRPC服务定义（user.proto）
syntax = "proto3";

package user;

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}

message GetUserRequest {
  int32 user_id = 1;
}

message GetUserResponse {
  int32 user_id = 1;
  string username = 2;
  string email = 3;
}

message CreateUserRequest {
  string username = 1;
  string email = 2;
  string password = 3;
}

message CreateUserResponse {
  int32 user_id = 1;
  bool success = 2;
}

# 5. 消息队列（RabbitMQ）
# 订单服务发送消息
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明队列
channel.queue_declare(queue='order_created')

# 发送消息
channel.basic_publish(
    exchange='',
    routing_key='order_created',
    body=json.dumps({'order_id': 123, 'user_id': 456})
)

# 库存服务消费消息
def callback(ch, method, properties, body):
    order = json.loads(body)
    # 扣减库存
    print(f"处理订单: {order['order_id']}")

channel.basic_consume(queue='order_created', on_message_callback=callback)
channel.start_consuming()

# 6. 熔断器（Hystrix）
# Python示例
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def call_order_service(order_id):
    # 调用订单服务
    response = requests.get(f'http://order-service:8002/orders/{order_id}')
    return response.json()

# 7. 分布式事务（Saga模式）
# 订单创建流程
def create_order_saga(user_id, product_id, quantity):
    try:
        # 步骤1: 创建订单
        order = create_order(user_id, product_id, quantity)

        # 步骤2: 扣减库存
        try:
            deduct_inventory(product_id, quantity)
        except Exception as e:
            # 补偿：取消订单
            cancel_order(order['order_id'])
            raise e

        # 步骤3: 扣减余额
        try:
            deduct_balance(user_id, order['amount'])
        except Exception as e:
            # 补偿：恢复库存、取消订单
            restore_inventory(product_id, quantity)
            cancel_order(order['order_id'])
            raise e

        return order
    except Exception as e:
        # 处理失败
        raise e

# 8. 链路追踪（Jaeger）
# Python示例
from jaeger_client import Config

config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
    },
    service_name='order-service',
)

tracer = config.initialize_tracer()

with tracer.start_span('create-order') as span:
    span.set_tag('user_id', user_id)
    # 业务逻辑
    order = create_order_logic(user_id, product_id, quantity)
    span.set_tag('order_id', order['order_id'])

# 9. 配置中心（Spring Cloud Config）
# application.yml
spring:
  cloud:
    config:
      uri: http://config-server:8888
      name: order-service
      profile: prod

# 10. 监控（Prometheus + Grafana）
# Prometheus配置
scrape_configs:
  - job_name: 'order-service'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['order-service:8002']

# 自定义指标
from prometheus_client import Counter, start_http_server

order_counter = Counter('orders_total', 'Total orders created')

def create_order(user_id, product_id, quantity):
    # 创建订单
    order = create_order_logic(user_id, product_id, quantity)
    # 增加计数
    order_counter.inc()
    return order''',
            "faq": [
                {
                    "question": "微服务和单体架构如何选择？",
                    "answer": "微服务适合：大型团队、复杂业务、需要独立部署和扩展；单体适合：小型团队、简单业务、快速迭代。不要为了微服务而微服务，过度拆分会增加复杂度。"
                },
                {
                    "question": "如何保证微服务的数据一致性？",
                    "answer": "1. 使用Saga模式实现最终一致性；2. 使用TCC（Try-Confirm-Cancel）模式；3. 使用消息队列实现异步补偿；4. 关键操作使用分布式事务（如Seata）。"
                }
            ],
            "references": [
                "微服务模式：https://microservices.io/",
                "Spring Cloud：https://spring.io/projects/spring-cloud",
                "Kubernetes文档：https://kubernetes.io/docs/"
            ]
        },
        "云原生技术实践": {
            "intro": "云原生是一种构建和运行应用程序的方法，充分利用云计算的优势。它包括容器化、服务网格、不可变基础设施、声明式API等概念。本文将介绍云原生的核心技术、架构设计、最佳实践以及如何构建可扩展、可观测的云原生应用。",
            "concepts": {
                "核心概念": [
                    "容器 - 轻量级、可移植的运行环境",
                    "服务网格 - 微服务间通信的基础设施层",
                    "不可变基础设施 - 不可变的部署单元",
                    "声明式API - 描述期望状态而非执行步骤"
                ],
                "关键术语": [
                    "Kubernetes - 容器编排平台",
                    "Istio - 服务网格实现",
                    "Helm - Kubernetes包管理器",
                    "Prometheus - 监控系统"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用Docker容器化应用",
                    "使用Kubernetes编排容器",
                    "配置健康检查和自动重启",
                    "使用ConfigMap和Secret管理配置"
                ],
                "高级技巧": [
                    "使用服务网格（Istio）管理流量",
                    "实现自动扩缩容（HPA）",
                    "配置蓝绿部署和金丝雀发布",
                    "实现可观测性（日志、指标、链路追踪）"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "应用无状态化，支持水平扩展",
                    "使用12-Factor App原则",
                    "实现优雅关闭，处理SIGTERM信号",
                    "配置资源限制，防止资源耗尽"
                ],
                "部署策略": [
                    "使用GitOps实现持续部署",
                    "配置多环境（dev、staging、prod）",
                    "实现自动化测试和部署流水线",
                    "配置灾备和故障转移"
                ]
            },
            "code_example": '''# 云原生技术实践示例

# 1. Kubernetes部署文件
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  labels:
    app: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: order-service:1.0.0
        ports:
        - containerPort: 8002
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: order-service-secret
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8002
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8002
          initialDelaySeconds: 5
          periodSeconds: 5

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8002
  type: ClusterIP

---
# hpa.yaml（自动扩缩容）
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

# 2. ConfigMap配置
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-service-config
data:
  application.yml: |
    server:
      port: 8002
    spring:
      datasource:
        url: ${DATABASE_URL}
    logging:
      level:
        root: INFO

# 3. Secret配置
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: order-service-secret
type: Opaque
data:
  database-url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0BkYjoxOTIzL29yZGVyZGI=

# 4. Istio服务网格配置
# virtualservice.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
  - order-service
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: order-service
        subset: v2
  - route:
    - destination:
        host: order-service
        subset: v1
      weight: 90
    - destination:
        host: order-service
        subset: v2
      weight: 10

---
# destinationrule.yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: order-service
spec:
  host: order-service
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2

# 5. Helm Chart示例
# Chart.yaml
apiVersion: v2
name: order-service
description: Order Service Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"

# values.yaml
replicaCount: 3
image:
  repository: order-service
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

# 6. Prometheus监控配置
# prometheus.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s

    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

# 7. Grafana Dashboard
# dashboard.json
{
  "dashboard": {
    "title": "Order Service Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}

# 8. 应用代码示例（优雅关闭）
# Python示例
import signal
import sys

class GracefulShutdown:
    def __init__(self):
        self.shutdown = False
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)

    def handle_shutdown(self, signum, frame):
        print(f"收到信号 {signum}, 准备关闭...")
        self.shutdown = True

# 使用
shutdown = GracefulShutdown()

while not shutdown.shutdown:
    # 处理请求
    process_request()

# 清理资源
cleanup()
print("服务已优雅关闭")

# 9. 健康检查端点
# Python示例
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/health')
def health():
    """存活探针"""
    return jsonify({'status': 'healthy'})

@app.route('/ready')
def ready():
    """就绪探针"""
    try:
        # 检查数据库连接
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return jsonify({'status': 'ready'})
    except Exception as e:
        return jsonify({'status': 'not ready', 'error': str(e)}), 503''',
            "faq": [
                {
                    "question": "云原生和传统部署有什么区别？",
                    "answer": "云原生使用容器化、服务网格、声明式API等技术，实现自动化、可扩展、可观测的应用；传统部署使用虚拟机或物理机，手动配置和管理。云原生更适合云环境，能充分利用云计算的优势。"
                },
                {
                    "question": "如何实现云原生的可观测性？",
                    "answer": "1. 使用Prometheus收集指标；2. 使用Grafana可视化监控；3. 使用ELK或Loki收集日志；4. 使用Jaeger或Zipkin实现链路追踪；5. 配置告警规则，及时发现异常。"
                }
            ],
            "references": [
                "CNCF云原生：https://www.cncf.io/",
                "Kubernetes文档：https://kubernetes.io/docs/",
                "12-Factor App：https://12factor.net/"
            ]
        },
        "DevOps自动化流程": {
            "intro": "DevOps通过自动化流程实现开发、测试、部署的高效协作，缩短交付周期，提高软件质量。本文将介绍CI/CD流水线、基础设施即代码、自动化测试、监控告警以及DevOps最佳实践，帮助你构建高效的DevOps体系。",
            "concepts": {
                "核心概念": [
                    "CI - 持续集成，频繁集成代码",
                    "CD - 持续部署，自动部署到生产",
                    "IaC - 基础设施即代码",
                    "GitOps - 使用Git作为单一事实来源"
                ],
                "关键术语": [
                    "Pipeline - 流水线，自动化流程",
                    "Artifact - 制品，构建产物",
                    "Environment - 环境，部署环境",
                    "Rollback - 回滚，恢复到之前版本"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用Git分支策略管理代码",
                    "配置自动化测试（单元测试、集成测试）",
                    "实现自动化构建和打包",
                    "配置自动化部署流水线"
                ],
                "高级技巧": [
                    "使用基础设施即代码管理环境",
                    "实现蓝绿部署和金丝雀发布",
                    "配置自动化回滚机制",
                    "实现监控告警和日志分析"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "遵循单一职责原则，每个阶段只做一件事",
                    "保持流水线快速，反馈及时",
                    "使用版本控制管理所有配置",
                    "定期审查和优化流水线"
                ],
                "部署策略": [
                    "使用多环境（dev、staging、prod）",
                    "实现自动化测试覆盖率监控",
                    "配置自动化安全扫描",
                    "实现自动化性能测试"
                ]
            },
            "code_example": '''# DevOps自动化流程示例

# 1. GitHub Actions CI/CD流水线
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .
        docker tag myapp:${{ github.sha }} myapp:latest

    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push myapp:${{ github.sha }}
        docker push myapp:latest

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to staging
      run: |
        kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n staging

  deploy-production:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n production

# 2. Jenkins Pipeline
# Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'pytest --cov=. --cov-report=html'
            }
            post {
                always {
                    publishHTML target: [
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ]
                }
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }

        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh 'kubectl set image deployment/myapp myapp=myapp:${BUILD_NUMBER} -n staging'
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
            }
            steps {
                input message: '确认部署到生产环境？', ok: '部署'
                sh 'kubectl set image deployment/myapp myapp=myapp:${BUILD_NUMBER} -n production'
            }
        }
    }

    post {
        success {
            echo '流水线执行成功'
        }
        failure {
            echo '流水线执行失败'
        }
    }
}

# 3. Terraform基础设施即代码
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
    Environment = "production"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "public-subnet"
  }
}

resource "aws_ecs_cluster" "main" {
  name = "main-cluster"
}

resource "aws_ecs_task_definition" "app" {
  family = "app"
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = "256"
  memory = "512"

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "myapp:latest"
      cpu       = 256
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 8000
        }
      ]
    }
  ])
}

# 4. Ansible配置管理
# playbook.yml
---
- name: Configure application server
  hosts: webservers
  become: yes

  tasks:
    - name: Install dependencies
      apt:
        name:
          - python3
          - python3-pip
          - nginx
        state: present

    - name: Create application directory
      file:
        path: /opt/myapp
        state: directory
        owner: www-data
        group: www-data

    - name: Copy application files
      copy:
        src: ./app/
        dest: /opt/myapp/
        owner: www-data
        group: www-data

    - name: Install Python dependencies
      pip:
        requirements: /opt/myapp/requirements.txt

    - name: Configure Nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/myapp
      notify:
        - Restart Nginx

    - name: Enable site
      file:
        src: /etc/nginx/sites-available/myapp
        dest: /etc/nginx/sites-enabled/myapp
        state: link
      notify:
        - Restart Nginx

  handlers:
    - name: Restart Nginx
      service:
        name: nginx
        state: restarted

# 5. 监控告警配置
# Prometheus告警规则
groups:
  - name: application_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "高错误率"
          description: "错误率超过5%: {{ $value }}"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "高响应时间"
          description: "P95响应时间超过1秒: {{ $value }}s"

      - alert: HighCPUUsage
        expr: rate(process_cpu_seconds_total[5m]) > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "高CPU使用率"
          description: "CPU使用率超过80%: {{ $value }}"

# 6. 自动化测试
# pytest示例
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """测试健康检查端点"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_create_order(client):
    """测试创建订单"""
    response = client.post('/api/orders', json={
        'user_id': 1,
        'product_id': 1,
        'quantity': 2
    })
    assert response.status_code == 201
    assert 'order_id' in response.json

def test_get_order(client):
    """测试获取订单"""
    # 先创建订单
    create_response = client.post('/api/orders', json={
        'user_id': 1,
        'product_id': 1,
        'quantity': 2
    })
    order_id = create_response.json['order_id']

    # 获取订单
    response = client.get(f'/api/orders/{order_id}')
    assert response.status_code == 200
    assert response.json['order_id'] == order_id

# 7. 蓝绿部署脚本
#!/bin/bash
# blue_green_deploy.sh

BLUE_PORT=8000
GREEN_PORT=8001
CURRENT_COLOR=$(curl -s http://lb/current_color)

if [ "$CURRENT_COLOR" = "blue" ]; then
    NEW_COLOR="green"
    NEW_PORT=$GREEN_PORT
else
    NEW_COLOR="blue"
    NEW_PORT=$BLUE_PORT
fi

echo "部署到 $NEW_COLOR 环境（端口 $NEW_PORT）"

# 部署新版本
kubectl set image deployment/myapp-$NEW_COLOR myapp=myapp:$VERSION

# 等待就绪
kubectl rollout status deployment/myapp-$NEW_COLOR

# 健康检查
for i in {1..30}; do
    if curl -f http://localhost:$NEW_PORT/health; then
        echo "健康检查通过"
        break
    fi
    sleep 2
done

# 切换流量
curl -X POST http://lb/switch_color -d "{\"color\": \"$NEW_COLOR\"}"

echo "部署完成，流量已切换到 $NEW_COLOR"''',
            "faq": [
                {
                    "question": "CI和CD有什么区别？",
                    "answer": "CI（持续集成）是频繁集成代码，自动构建和测试；CD（持续部署）是自动部署到生产环境。CI关注代码质量和集成，CD关注交付和部署。CI是CD的基础，先有CI再有CD。"
                },
                {
                    "question": "如何实现零停机部署？",
                    "answer": "1. 使用蓝绿部署，同时运行两个版本，切换流量；2. 使用金丝雀发布，逐步放量；3. 使用滚动更新，逐个替换实例；4. 配置健康检查，确保新版本正常后再切换流量。"
                }
            ],
            "references": [
                "Jenkins文档：https://www.jenkins.io/doc/",
                "GitHub Actions：https://docs.github.com/en/actions",
                "Terraform文档：https://www.terraform.io/docs"
            ]
        },
        "人工智能应用开发": {
            "intro": "人工智能正在改变各行各业，从图像识别到自然语言处理，从推荐系统到自动驾驶。本文将介绍AI应用开发的核心技术、常用框架、模型训练、部署优化以及实际应用场景，帮助你快速入门AI开发。",
            "concepts": {
                "核心概念": [
                    "机器学习 - 从数据中学习模式",
                    "深度学习 - 使用神经网络学习",
                    "监督学习 - 有标签数据训练",
                    "无监督学习 - 无标签数据训练"
                ],
                "关键术语": [
                    "模型 - 训练好的算法",
                    "特征 - 数据的属性",
                    "训练 - 学习模型参数",
                    "推理 - 使用模型预测"
                ]
            },
            "practices": {
                "基础技巧": [
                    "使用scikit-learn进行传统机器学习",
                    "使用TensorFlow/PyTorch进行深度学习",
                    "使用pandas处理数据",
                    "使用matplotlib可视化数据"
                ],
                "高级技巧": [
                    "使用预训练模型（Transfer Learning）",
                    "使用GPU加速训练",
                    "实现模型量化和剪枝",
                    "使用ONNX进行模型部署"
                ]
            },
            "best_practices": {
                "开发规范": [
                    "划分训练集、验证集、测试集",
                    "使用交叉验证评估模型",
                    "记录超参数和实验结果",
                    "版本控制模型和数据"
                ],
                "部署策略": [
                    "使用TensorFlow Serving或TorchServe部署",
                    "使用Docker容器化模型服务",
                    "实现模型A/B测试",
                    "监控模型性能和数据漂移"
                ]
            },
            "code_example": '''# AI应用开发示例

# 1. 传统机器学习（scikit-learn）
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# 加载数据
data = pd.read_csv('iris.csv')
X = data.drop('species', axis=1)
y = data['species']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 训练模型
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
print(f"准确率: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

# 2. 深度学习（PyTorch）
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# 定义模型
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# 准备数据
X_train_tensor = torch.FloatTensor(X_train.values)
y_train_tensor = torch.LongTensor(y_train.astype('category').cat.codes.values)
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 初始化模型
model = SimpleNN(input_size=4, hidden_size=16, num_classes=3)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练
num_epochs = 100
for epoch in range(num_epochs):
    for batch_X, batch_y in train_loader:
        # 前向传播
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 3. 图像分类（使用预训练模型）
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image

# 加载预训练模型
model = models.resnet18(pretrained=True)
model.eval()

# 图像预处理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 加载图像
image = Image.open('image.jpg')
input_tensor = preprocess(image)
input_batch = input_tensor.unsqueeze(0)  # 添加batch维度

# 预测
with torch.no_grad():
    output = model(input_batch)

# 获取预测结果
probabilities = torch.nn.functional.softmax(output[0], dim=0)
with open('imagenet_classes.txt') as f:
    categories = [s.strip() for s in f.readlines()]

top5_prob, top5_catid = torch.topk(probabilities, 5)
for i in range(top5_prob.size(0)):
    print(categories[top5_catid[i]], top5_prob[i].item())

# 4. 自然语言处理（使用Hugging Face）
from transformers import pipeline

# 文本分类
classifier = pipeline('sentiment-analysis')
result = classifier("I love this product!")
print(result)  # [{'label': 'POSITIVE', 'score': 0.9998}]

# 文本生成
generator = pipeline('text-generation', model='gpt2')
text = generator("Once upon a time", max_length=50)
print(text[0]['generated_text'])

# 问答
qa_pipeline = pipeline('question-answering')
context = "Python is a high-level programming language."
result = qa_pipeline(question="What is Python?", context=context)
print(result['answer'])  # "a high-level programming language"

# 5. 模型部署（Flask API）
from flask import Flask, request, jsonify
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

app = Flask(__name__)

# 加载模型
model = torch.load('model.pth')
model.eval()

# 预处理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

@app.route('/predict', methods=['POST'])
def predict():
    # 接收图像
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))

    # 预处理
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # 预测
    with torch.no_grad():
        output = model(input_batch)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)

    # 返回结果
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    results = []
    for i in range(top5_prob.size(0)):
        results.append({
            'class': top5_catid[i].item(),
            'probability': top5_prob[i].item()
        })

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# 6. 模型优化（量化）
import torch

# 加载模型
model = torch.load('model.pth')

# 量化模型
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},  # 量化Linear层
    dtype=torch.qint8
)

# 保存量化模型
torch.save(quantized_model, 'quantized_model.pth')

# 7. 数据增强
from torchvision import transforms

# 训练时的数据增强
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomResizedCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 测试时不做数据增强
test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 8. 超参数调优（使用Optuna）
import optuna

def objective(trial):
    # 定义超参数搜索空间
    n_estimators = trial.suggest_int('n_estimators', 10, 100)
    max_depth = trial.suggest_int('max_depth', 2, 32)
    learning_rate = trial.suggest_float('learning_rate', 0.01, 0.1)

    # 训练模型
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 评估
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy

# 运行优化
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# 输出最佳参数
print(f"最佳准确率: {study.best_value:.2f}")
print(f"最佳参数: {study.best_params}")''',
            "faq": [
                {
                    "question": "机器学习和深度学习有什么区别？",
                    "answer": "机器学习使用传统算法（如决策树、SVM），需要手动提取特征；深度学习使用神经网络，可以自动学习特征。深度学习适合处理图像、文本等复杂数据，但需要大量数据和计算资源。"
                },
                {
                    "question": "如何选择合适的AI模型？",
                    "answer": "1. 根据任务类型选择（分类、回归、聚类等）；2. 考虑数据量和质量；3. 评估模型复杂度和可解释性；4. 考虑计算资源和部署环境；5. 从简单模型开始，逐步尝试复杂模型。"
                }
            ],
            "references": [
                "scikit-learn文档：https://scikit-learn.org/",
                "PyTorch教程：https://pytorch.org/tutorials/",
                "Hugging Face：https://huggingface.co/docs"
            ]
        }
    }

    return content_map.get(topic, None)

def step_1_generate_html(topic):
    """第1步：生成HTML文档"""
    logger.log(f"📝 步骤 1/3: 生成HTML文档")

    try:
        today = datetime.now().strftime("%Y%m%d")
        today_str = datetime.now().strftime("%Y年%m月%d日")
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")

        # 获取主题内容
        content = get_topic_content(topic)
        if not content:
            logger.log(f"❌ 未找到主题内容: {topic}")
            return None

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
            <p>{content['intro']}</p>

            <h2>一、基本概念</h2>

            <p>了解{topic}的基本概念是掌握该技术的基础。本节将介绍核心概念和关键术语。</p>

            <h3>1.1 核心概念</h3>
            <ul>
'''

        # 添加核心概念
        for concept in content['concepts']['核心概念']:
            html_content += f'                <li>{concept}</li>\n'

        html_content += '''            </ul>

            <h3>1.2 关键术语</h3>
            <ul>
'''

        # 添加关键术语
        for term in content['concepts']['关键术语']:
            html_content += f'                <li>{term}</li>\n'

        html_content += '''            </ul>

            <h2>二、实践技巧</h2>

            <p>掌握{topic}的实践技巧可以帮助您更好地应用该技术。</p>

            <h3>2.1 基础技巧</h3>
            <ul>
'''

        # 添加基础技巧
        for tip in content['practices']['基础技巧']:
            html_content += f'                <li>{tip}</li>\n'

        html_content += '''            </ul>

            <h3>2.2 高级技巧</h3>
            <ul>
'''

        # 添加高级技巧
        for tip in content['practices']['高级技巧']:
            html_content += f'                <li>{tip}</li>\n'

        html_content += '''            </ul>

            <h2>三、最佳实践</h2>

            <p>遵循{topic}的最佳实践可以确保项目的成功和可维护性。</p>

            <h3>3.1 开发规范</h3>
            <ul>
'''

        # 添加开发规范
        for practice in content['best_practices']['开发规范']:
            html_content += f'                <li>{practice}</li>\n'

        html_content += '''            </ul>

            <h3>3.2 部署策略</h3>
            <ul>
'''

        # 添加部署策略
        for strategy in content['best_practices']['部署策略']:
            html_content += f'                <li>{strategy}</li>\n'

        html_content += '''            </ul>

            <h2>四、代码示例</h2>

            <p>以下是一些{topic}的代码示例，帮助您更好地理解和应用。</p>

            <pre><code>''' + content['code_example'] + '''</code></pre>

            <h2>五、常见问题</h2>
'''

        # 添加常见问题
        for i, faq in enumerate(content['faq'], 1):
            html_content += f'''            <h3>5.{i} {faq['question']}</h3>

            <p><strong>问题描述：</strong>{faq['question']}</p>

            <p><strong>解决方案：</strong>{faq['answer']}</p>

'''

        html_content += '''            <h2>六、总结</h2>

            <p>通过本文的学习，您应该对{topic}有了更深入的理解。掌握这些知识和技巧，可以帮助您在实际项目中更好地应用{topic}。</p>

            <h2>七、参考资料</h2>

            <ul>
'''

        # 添加参考资料
        for ref in content['references']:
            html_content += f'                <li>{ref}</li>\n'

        html_content += '''            </ul>
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

        # 替换所有{topic}变量
        html_content = html_content.replace('{topic}', topic)

        # 保存HTML文件
        output_path = Path(BLOG_PATH) / f"history/{year}/{month}/{today}.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.log(f"✅ HTML文档已生成: {output_path}")
        return str(output_path)

    except Exception as e:
        logger.log(f"❌ HTML生成失败: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return None

def step_2_generate_image(topic, seed=101, max_retries=2):
    """第2步：生成图片（参考环球新闻的图片生成逻辑）"""
    logger.log(f"🎨 步骤 2/3: 生成图片")
    logger.log(f"📊 质量标准: 文件200KB-800KB, 分辨率≥1280x720, 比例16:9")

    try:
        results = []
        genai_script = Path("/home/swg/.openclaw/workspace/skills/nvidia-genai/generate.py")

        # 生成提示词（参考环球新闻的提示词）
        prompt = f"超高清真实技术文档封面，{topic}，8K分辨率，专业技术摄影，极致清晰，锐利细节，真实光线，自然色彩，电影级构图，科技感，现代感，专业镜头，景深效果，真实场景，无卡通，无插画，照片级质量，技术文档风格，专业摄影标准"

        # 图片文件名
        image_file = IMAGES_DIR / f"tech_{seed}.png"

        success = False
        retry_count = 0

        while not success and retry_count <= max_retries:
            try:
                logger.log(f"🖼️  生成图片: {topic[:30]}... (尝试 {retry_count + 1})")

                result = subprocess.run(
                    ["python3", str(genai_script), prompt,
                     "--model", "stabilityai/stable-diffusion-3-medium",
                     "--ratio", "16:9",
                     "--steps", "50",  # 提高到50步，增强细节
                     "--cfg", "7.5",  # 提高CFG值，增强提示词遵循度
                     "--seed", str(seed + retry_count * 100),
                     "--output", str(image_file)],
                    capture_output=True,
                    text=True,
                    timeout=240,  # 增加超时时间
                    env={**os.environ, "NVIDIA_API_KEY": NVIDIA_API_KEY}
                )

                if result.returncode == 0 and image_file.exists():
                    # 检查图片质量
                    quality_ok = check_image_quality(image_file)
                    if quality_ok:
                        logger.log(f"✅ 图片生成成功且质量合格")
                        results.append(str(image_file))
                        success = True
                    else:
                        if retry_count < max_retries:
                            logger.log(f"⚠️  图片质量不达标，重新生成...")
                            retry_count += 1
                            image_file.unlink()  # 删除不合格的图片
                        else:
                            logger.log(f"⚠️  图片质量未达标但已达到最大重试次数")
                            results.append(str(image_file))
                            success = True
                else:
                    if retry_count < max_retries:
                        logger.log(f"⚠️  图片生成失败，重试...")
                        retry_count += 1
                    else:
                        logger.log(f"❌ 图片生成失败")
                        results.append(None)
                        success = True

                # 稍等避免API限流
                if not success:
                    time.sleep(3)

            except subprocess.TimeoutExpired:
                if retry_count < max_retries:
                    logger.log(f"⚠️  图片生成超时，重试...")
                    retry_count += 1
                else:
                    logger.log(f"❌ 图片生成超时")
                    results.append(None)
                    success = True
            except Exception as e:
                if retry_count < max_retries:
                    logger.log(f"⚠️  图片生成异常: {str(e)}，重试...")
                    retry_count += 1
                else:
                    logger.log(f"❌ 图片生成最终失败")
                    results.append(None)
                    success = True

        return results[0] if results else None
    except Exception as e:
        logger.log(f"❌ 图片生成异常: {str(e)}")
        return None

def check_image_quality(image_path):
    """检查图片质量是否达标（参考环球新闻的质量检查）"""
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size
            file_size_kb = os.path.getsize(image_path) / 1024

            # 质量标准
            min_size_kb = 200
            max_size_kb = 800
            min_width = 1280
            min_height = 720
            target_ratio = 16/9
            ratio_tolerance = 0.1

            ratio = width / height
            ratio_diff = abs(ratio - target_ratio) / target_ratio

            # 检查各项指标
            size_ok = min_size_kb <= file_size_kb <= max_size_kb
            resolution_ok = width >= min_width and height >= min_height
            ratio_ok = ratio_diff <= ratio_tolerance

            return size_ok and resolution_ok and ratio_ok
    except:
        return False

def step_3_update_index(topic, image_file):
    """第3步：更新首页"""
    logger.log(f"🔄 步骤 3/3: 更新首页")

    try:
        today_str = datetime.now().strftime("%Y年%m月%d日")
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")
        today = datetime.now().strftime("%Y%m%d")

        # 获取主题内容
        content = get_topic_content(topic)
        if not content:
            logger.log(f"❌ 未找到主题内容: {topic}")
            return False

        # 读取首页
        index_path = Path(BLOG_PATH) / "index.html"
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()

        # 提取今日推荐部分
        image_path = f"images/{Path(image_file).name}" if image_file else "images/tech_default.png"

        # 生成要点列表
        points_html = ""
        for i, point in enumerate(content['practices']['基础技巧'][:3], 1):
            points_html += f'                    <li>{point}</li>\n'

        today_section = f'''            <h2>今日推荐-{today_str}</h2>

            <div style="background: linear-gradient(145deg, #f6f8fa 0%, #ffffff 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 2px solid #667eea;">
                <img src="{image_path}" alt="{topic}" style="width: 100%; max-height: 300px; object-fit: cover; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #667eea; margin-bottom: 15px; font-size: 1.5em;">{topic}</h3>
                <p style="margin-bottom: 15px;">{content['intro']}</p>
                <p style="margin-bottom: 15px;"><strong>主要内容：</strong></p>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
{points_html}                </ul>
                <a href="history/{year}/{month}/{today}.html" style="color: #667eea; font-weight: bold;">阅读完整文章 →</a>
            </div>'''

        # 查找并替换今日推荐部分
        pattern = r'<h2>今日推荐-.*?</h2>.*?<h2>历史存档</h2>'
        replacement = today_section + '\n\n            <h2>历史存档</h2>'

        new_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

        # 写回
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        logger.log("✅ 首页已更新")
        return True

    except Exception as e:
        logger.log(f"❌ 首页更新失败: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return False

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="技术文档自动更新（带图片生成）")
    parser.add_argument("--no-upload", action="store_true", help="不上传，仅生成")
    parser.add_argument("--seed", type=int, default=101, help="图片随机种子")

    args = parser.parse_args()

    try:
        logger.log("=" * 60)
        logger.log("📝 技术文档自动更新")
        logger.log(f"📅 日期: {datetime.now().strftime('%Y年%m月%d日')}")
        logger.log("=" * 60)

        # 获取技术主题
        topic = get_tech_topic()
        logger.log(f"🎯 主题: {topic}")

        # 第1步：生成HTML文档
        html_file = step_1_generate_html(topic)
        if not html_file:
            return 1

        # 第2步：生成图片
        image_file = step_2_generate_image(topic, args.seed)

        # 第3步：更新首页
        success = step_3_update_index(topic, image_file)
        if not success:
            return 1

        # Git提交
        if not args.no_upload:
            logger.log("📝 正在提交到Git...")

            result = subprocess.run(
                ["git", "add", "."],
                cwd=BLOG_PATH,
                capture_output=True,
                text=True
            )

            result = subprocess.run(
                ["git", "commit", "-m", f"Auto: 技术文档自动更新 - {datetime.now().strftime('%Y年%m月%d日')}\n\n- 主题: {topic}\n- 生成技术文档\n- 生成封面图片\n- 更新首页推荐"],
                cwd=BLOG_PATH,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.log("✅ Git提交成功")

                # 推送到GitHub
                result = subprocess.run(
                    ["git", "push"],
                    cwd=BLOG_PATH,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    logger.log("✅ 推送到GitHub成功")
                else:
                    logger.log("⚠️  推送到GitHub失败")
            else:
                logger.log("⚠️  没有新的更改需要提交")

        logger.log("=" * 60)
        logger.log("✅ 技术文档自动更新完成！")
        logger.log(f"📅 日期: {datetime.now().strftime('%Y年%m月%d日')}")
        logger.log(f"🎯 主题: {topic}")
        logger.log(f"🖼️  图片: {'✅ 已生成' if image_file else '❌ 生成失败'}")
        logger.log("=" * 60)

        return 0

    except Exception as e:
        logger.log(f"❌ 错误: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
