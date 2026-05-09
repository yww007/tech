#!/usr/bin/env python3
"""
技术文档配图重新生成 - 基于当前文章内容
支持动态主题：python3 regenerate_tech_images.py "AI主题描述"
"""

import subprocess
import time
import sys
from pathlib import Path
from PIL import Image

SKILL_DIR = Path("/home/swg/.openclaw/workspace/skills/nvidia-genai")
POLLINATIONS_SCRIPT = Path("/home/swg/.openclaw/workspace/news-blog/pollinations_generate.py")
OUTPUT_DIR = Path("/home/swg/.openclaw/workspace/tech/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_image_prompts(topic="AI驱动的网络安全"):
    """根据主题获取图片提示词"""
    
    # 通用科技/安全主题背景图
    bg_prompts = {
        "default": "Futuristic cybersecurity technology background, dark blue digital network, glowing circuit patterns, secure internet infrastructure, holographic security shields, abstract tech aesthetic, 8k high resolution",
    }
    
    # 基于主题生成内容配图提示词
    content_prompts = [
        {
            "id": "101",
            "filename": "tech_101.png",
            "title": "技术架构图",
            "prompt_en": "Professional technical architecture diagram, system components connected with lines, cloud infrastructure, servers and databases, modern tech infographic, clean design with blue accents",
        },
        {
            "id": "102", 
            "filename": "tech_102.png",
            "title": "技术应用场景",
            "prompt_en": "Technology application scenarios, multiple use cases displayed, practical implementations in real world, professional tech environment, detailed illustrations",
        },
        {
            "id": "202",
            "filename": "tech_202.png", 
            "title": "工作流程图",
            "prompt_en": "Technical workflow diagram, step by step process with arrows, data flowing through system, professional flowchart style, clean and organized layout",
        },
        {
            "id": "430",
            "filename": "tech_430.png",
            "title": "深度学习架构",
            "prompt_en": "Deep learning neural network architecture visualization, multi-layer processing units, data transformation stages, AI model structure, futuristic tech illustration",
        },
        {
            "id": "504",
            "filename": "tech_504.png",
            "title": "自动化流程",
            "prompt_en": "Automated process workflow, robotic process automation RPA, AI handling tasks automatically, efficiency optimization, modern automation concept",
        },
        {
            "id": "505",
            "filename": "tech_505.png",
            "title": "实施框架",
            "prompt_en": "Implementation framework diagram, structured approach with phases, strategic planning, enterprise deployment model, professional methodology visualization",
        },
        {
            "id": "501",
            "filename": "tech_501.png",
            "title": "未来趋势",
            "prompt_en": "Future technology trends concept, next generation innovation, emerging technologies converging, forward-looking tech vision, cutting-edge development illustration",
        },
    ]
    
    return {
        "bg": {
            "id": "bg",
            "filename": "website-background-8k.png",
            "title": "背景图",
            "prompt_en": bg_prompts["default"],
            "width": 1920,
            "height": 1080,
        },
        "content": content_prompts
    }

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
        "--width", str(image_info.get("width", 800)),
        "--height", str(image_info.get("height", 450)),
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
    # 获取主题（可选命令行参数）
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI驱动的网络安全"
    
    # 获取图片列表
    prompts = get_image_prompts(topic)
    images = [prompts["bg"]] + prompts["content"]
    
    print(f"开始重新生成 {len(images)} 张技术文档配图...")
    print(f"主题: {topic}")
    print(f"每张间隔 60 秒避免限流，总耗时约 {len(images)} 分钟\n")
    
    success = 0
    failed = []
    
    for i, img in enumerate(images):
        print(f"[{i+1}/{len(images)}]")
        if generate_with_pollinations(img):
            success += 1
        else:
            failed.append(img["id"])
        
        # 每张间隔60秒避免限流
        if i < len(images) - 1:
            print(f"  等待 60 秒...")
            time.sleep(60)
    
    print(f"\n完成！成功 {success}/{len(images)}")
    if failed:
        print(f"失败: {failed}")