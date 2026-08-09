#!/usr/bin/env python3
"""
智谱 CogView-3-Flash 图片生成脚本
Usage: python3 zhipu_generate.py "prompt" --output /path/to/output.png --width 1024 --height 1024
"""

import os
import sys
import argparse
import urllib.request
import json
from pathlib import Path


def generate_image(prompt, output_path, width=1024, height=1024, api_key=None):
    """通过智谱 CogView-3-Flash API 生成图片"""

    if api_key is None:
        # 从配置文件读取
        api_key = os.environ.get("ZHIPU_API_KEY", "5697b9462d534279be02cdc530363258.CZVNuSV8NERVbbci")

    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }

    print(f"🎨 Generating image...")
    print(f"   Prompt: {prompt[:60]}...")
    print(f"   Size: {width}x{height}")

    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })

        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())

        img_url = result["choices"][0]["message"]["content"][0]["url"]

        # 下载图片
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(img_url, output_path)

        size_kb = output_path.stat().st_size / 1024
        print(f"✅ 图片已保存: {output_path} ({size_kb:.0f} KB)")
        return True

    except urllib.error.HTTPError as e:
        print(f"❌ HTTP 错误: {e.code}")
        try:
            error_body = e.read().decode()
            print(f"   详情: {error_body[:200]}")
        except Exception:
            pass
        return False
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="智谱 CogView-3-Flash 图片生成")
    parser.add_argument("prompt", help="图片描述提示词")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--width", type=int, default=1024, help="图片宽度")
    parser.add_argument("--height", type=int, default=1024, help="图片高度")
    parser.add_argument("--api-key", default=None, help="API密钥（可选，默认使用配置）")

    args = parser.parse_args()

    success = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        width=args.width,
        height=args.height,
        api_key=args.api_key
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()