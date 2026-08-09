#!/usr/bin/env python3
"""并行生成8张云原生架构图片"""
import os
import sys
import urllib.request
import json
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = os.environ.get("ZHIPU_API_KEY", "5697b9462d534279be02cdc530363258.CZVNuSV8NERVbbci")
URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

IMAGES = [
    ("images/tech_home_1_new.png", "云原生架构 科技感 现代数据中心 暗色背景 插画风格 4K高清", 1024, 576),
    ("images/tech_home_2_new.png", "Kubernetes容器编排平台 科技感 微服务集群 暗色背景 插画风格 4K高清", 1024, 1024),
    ("images/tech_home_3_new.png", "云原生可观测性 监控仪表盘 数据可视化 科技感 暗色背景 插画风格 4K高清", 1024, 1024),
    ("images/tech_home_4_new.png", "DevOps CI/CD流水线 自动化部署 科技感 暗色背景 插画风格 4K高清", 1024, 1024),
    ("images/tech_home_5_new.png", "Service Mesh服务网格 科技感 暗色背景 插画风格 4K高清", 1024, 1024),
    ("images/tech_home_6_new.png", "容器安全 Docker K8s 科技感 暗色背景 插画风格 4K高清", 1024, 1024),
    ("images/tech_home_7_new.png", "GitOps工作流 基础设施即代码 科技感 暗色背景 插画风格 4K高清", 1024, 1024),
    ("images/tech_home_8_new.png", "边缘计算 IoT设备 云原生 科技感 暗色背景 插画风格 4K高清", 1024, 1024),
]

def generate_one(output_path, prompt, width, height):
    print(f"🎨 Generating {output_path}...")
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(URL, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        })
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
        img_url = result["choices"][0]["message"]["content"][0]["url"]
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(img_url, output_path)
        print(f"✅ {output_path} done")
        return True
    except Exception as e:
        print(f"❌ {output_path} failed: {e}")
        return False

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(generate_one, path, prompt, w, h) for path, prompt, w, h in IMAGES]
    for f in as_completed(futures):
        pass

print("\n全部完成！")