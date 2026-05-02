#!/usr/bin/env python3
"""
Pollinations AI 图片生成脚本
Usage: python3 pollinations_generate.py "prompt" --output /path/to/output.png
"""

import os
import sys
import argparse
import requests
import urllib.parse
from pathlib import Path


def generate_image(prompt, output_path, width=1344, height=768, seed=None):
    """通过 Pollinations API 生成图片"""

    # URL编码提示词
    encoded_prompt = urllib.parse.quote(prompt)

    # 构建URL
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"

    print(f"🎨 Generating image...")
    print(f"   URL: {url}")
    print(f"   Size: {width}x{height}")

    try:
        response = requests.get(url, timeout=300)

        if response.status_code != 200:
            print(f"❌ API 错误: {response.status_code}")
            return False

        # 保存图片
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 检查是否是JPEG格式（Pollinations API有时返回JPEG但扩展名是PNG）
        content_type = response.headers.get('content-type', '')
        is_jpeg = 'jpeg' in content_type.lower() or 'jpg' in content_type.lower()

        # 如果是JPEG，转换为PNG
        if is_jpeg or b'JFIF' in response.content[:10] or b'Exif' in response.content[:10]:
            from PIL import Image
            import io

            # 使用PIL打开JPEG并保存为PNG
            img = Image.open(io.BytesIO(response.content))
            img.save(output_path, 'PNG')
            print(f"🔄 转换JPEG为PNG")
        else:
            # 直接保存
            with open(output_path, "wb") as f:
                f.write(response.content)

        size_kb = len(response.content) / 1024
        print(f"✅ 图片已保存: {output_path} ({size_kb:.0f} KB)")
        return True

    except requests.exceptions.Timeout:
        print(f"❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Pollinations AI 图片生成")
    parser.add_argument("prompt", help="图片描述提示词")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--width", type=int, default=1344, help="图片宽度")
    parser.add_argument("--height", type=int, default=768, help="图片高度")
    parser.add_argument("--seed", type=int, default=101, help="随机种子")

    args = parser.parse_args()

    success = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        width=args.width,
        height=args.height,
        seed=args.seed
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
