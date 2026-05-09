#!/usr/bin/env python3
"""
技术文档配图重新生成 - 基于当前文章内容
"""

import subprocess
import time
from pathlib import Path
from PIL import Image

SKILL_DIR = Path("/home/swg/.openclaw/workspace/skills/nvidia-genai")
POLLINATIONS_SCRIPT = Path("/home/swg/.openclaw/workspace/news-blog/pollinations_generate.py")
OUTPUT_DIR = Path("/home/swg/.openclaw/workspace/tech/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 当前文章是 "AI驱动的网络安全防护体系"
# 需要生成 7 张配图 + 1 张背景图

IMAGES = [
    # 背景图
    {
        "id": "bg",
        "filename": "website-background-8k.png",
        "title": "背景图",
        "prompt_en": "Futuristic cybersecurity technology background, dark blue digital network, glowing circuit patterns, secure internet infrastructure, holographic security shields, abstract tech aesthetic, 8k high resolution",
        "width": 1920,
        "height": 1080,
    },
    # 内容配图
    {
        "id": "101",
        "filename": "tech_101.png",
        "title": "AI网络安全架构图",
        "prompt_en": "AI network security architecture diagram, central AI brain processing data streams, firewalls and security layers visualized, interconnected nodes, modern tech infographic style, blue and cyan color scheme",
        "width": 800,
        "height": 450,
    },
    {
        "id": "102",
        "filename": "tech_102.png",
        "title": "AI安全应用场景",
        "prompt_en": "AI cybersecurity application scenarios, multiple screens showing threat detection, automated response systems, machine learning models, data analytics dashboards, professional tech environment",
        "width": 800,
        "height": 450,
    },
    {
        "id": "202",
        "filename": "tech_202.png",
        "title": "机器学习威胁检测流程",
        "prompt_en": "Machine learning threat detection workflow diagram, data input flowing through neural network layers, threat patterns being identified, flow chart with icons, clean professional design",
        "width": 800,
        "height": 450,
    },
    {
        "id": "430",
        "filename": "tech_430.png",
        "title": "深度学习架构",
        "prompt_en": "Deep learning security analysis architecture, neural network visualization with security shield, multi-layer processing, data streams, futuristic tech illustration, dark theme with glowing elements",
        "width": 800,
        "height": 450,
    },
    {
        "id": "504",
        "filename": "tech_504.png",
        "title": "自动化响应流程",
        "prompt_en": "Automated security response workflow, AI system detecting threats and automatically deploying countermeasures, flowchart with robotic process automation, incident response diagram",
        "width": 800,
        "height": 450,
    },
    {
        "id": "505",
        "filename": "tech_505.png",
        "title": "AI安全实施框架",
        "prompt_en": "AI security implementation framework, layered security model with AI at center, implementation stages diagram, strategic planning visualization, enterprise security architecture",
        "width": 800,
        "height": 450,
    },
    {
        "id": "501",
        "filename": "tech_501.png",
        "title": "未来发展趋势",
        "prompt_en": "Future AI cybersecurity trends, holographic displays showing quantum computing and AI convergence, next generation security technology, forward-looking tech concept illustration",
        "width": 800,
        "height": 450,
    },
]

def generate_with_pollinations(image_info):
    """使用 Pollinations 生成图片"""
    output_file = OUTPUT_DIR / image_info["filename"]
    
    print(f"[{image_info['id']}] 生成: {image_info['title']}")
    print(f"     Prompt: {image_info['prompt_en'][:60]}...")
    
    cmd = [
        "python3",
        str(POLLINATIONS_SCRIPT),
        image_info["prompt_en"],
        "--output", str(output_file),
        "--width", str(image_info["width"]),
        "--height", str(image_info["height"]),
        "--model", "turbo",
        "--nologo",
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
        )
        
        if result.returncode == 0 and output_file.exists():
            size = output_file.stat().st_size / 1024
            print(f"  ✅ 成功 ({size:.0f}KB)")
            
            # 验证是真正的 PNG
            try:
                with Image.open(output_file) as img:
                    if img.format != 'PNG' or img.mode not in ('RGB', 'RGBA'):
                        print(f"  ⚠️ 格式验证失败: {img.format} {img.mode}")
                        return False
            except Exception as e:
                print(f"  ⚠️ 图片验证失败: {e}")
                return False
            
            return True
        else:
            print(f"  ❌ 失败: {result.stderr[:200] if result.stderr else 'Unknown error'}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ❌ 超时")
        return False
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        return False

if __name__ == "__main__":
    print(f"开始重新生成 {len(IMAGES)} 张技术文档配图...")
    print(f"每张间隔 60 秒避免限流，总耗时约 {len(IMAGES)} 分钟\n")
    
    success = 0
    failed = []
    
    for i, img in enumerate(IMAGES):
        print(f"[{i+1}/{len(IMAGES)}]")
        if generate_with_pollinations(img):
            success += 1
        else:
            failed.append(img["id"])
        
        # 每张间隔60秒避免限流
        if i < len(IMAGES) - 1:
            print(f"  等待 60 秒...")
            time.sleep(60)
    
    print(f"\n完成！成功 {success}/{len(IMAGES)}")
    if failed:
        print(f"失败: {failed}")