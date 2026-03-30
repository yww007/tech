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
    """获取技术主题"""
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

    import random
    return random.choice(TECH_TOPICS)

def step_1_generate_html(topic):
    """第1步：生成HTML文档"""
    logger.log(f"📝 步骤 1/3: 生成HTML文档")

    try:
        today = datetime.now().strftime("%Y%m%d")
        today_str = datetime.now().strftime("%Y年%m月%d日")
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")

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

        # 读取首页
        index_path = Path(BLOG_PATH) / "index.html"
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取今日推荐部分
        image_path = f"images/{Path(image_file).name}" if image_file else "images/tech_default.png"

        today_section = f'''            <h2>今日推荐-{today_str}</h2>

            <div style="background: linear-gradient(145deg, #f6f8fa 0%, #ffffff 100%); padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 2px solid #667eea;">
                <img src="{image_path}" alt="{topic}" style="width: 100%; max-height: 300px; object-fit: cover; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #667eea; margin-bottom: 15px; font-size: 1.5em;">{topic}</h3>
                <p style="margin-bottom: 15px;">本文将详细介绍{topic}的相关知识，包括基本概念、实践技巧和最佳实践。</p>
                <p style="margin-bottom: 15px;"><strong>主要内容：</strong></p>
                <ul style="margin-left: 20px; margin-bottom: 15px;">
                    <li>基本概念 - 核心概念和关键术语</li>
                    <li>实践技巧 - 基础技巧和高级技巧</li>
                    <li>最佳实践 - 开发规范和部署策略</li>
                    <li>代码示例 - 实用的代码示例</li>
                    <li>常见问题 - 常见问题和解决方案</li>
                </ul>
                <a href="history/{year}/{month}/{today}.html" style="color: #667eea; font-weight: bold;">阅读完整文章 →</a>
            </div>'''

        # 查找并替换今日推荐部分
        pattern = r'<h2>今日推荐-.*?</h2>.*?<h2>历史存档</h2>'
        replacement = today_section + '\n\n            <h2>历史存档</h2>'

        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

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
