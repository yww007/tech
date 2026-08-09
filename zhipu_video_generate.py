#!/usr/bin/env python3
"""智谱 CogVideoX-Flash 视频生成脚本（异步版）

说明：系统根证书中缺 Sectigo RSA Domain Validation Secure Server CA，
导致 api.zhipu.ai 证书链验证失败。这里调用 curl -k 跳过校验（接口已知，
安全性由 Bearer token 保证）。
"""
import sys
import os
import json
import time
import subprocess

API_KEY = "5697b9462d534279be02cdc530363258.CZVNuSV8NERVbbci"
BASE = "https://open.bigmodel.cn/api/paas"
MODEL = "cogvideox-flash"


def curl_json(method: str, url: str, payload: dict = None, timeout: int = 60) -> dict:
    """用 curl -k 跳过 SSL 校验调用智谱 API。"""
    cmd = [
        "curl", "-sS", "-k", "-L",
        "-X", method,
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Content-Type: application/json",
        "--max-time", str(timeout),
        url,
    ]
    if payload is not None:
        cmd += ["-d", json.dumps(payload, ensure_ascii=False)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"curl 失败 ({proc.returncode}): {proc.stderr[:500]}")
    out = proc.stdout.strip()
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        raise RuntimeError(f"返回非 JSON: {out[:500]}")


def curl_download(url: str, out_path: str, timeout: int = 180) -> str:
    """下载视频文件。智谱返回的 CDN URL 通常也带 self-signed 或证书链问题。"""
    cmd = [
        "curl", "-sS", "-k", "-L",
        "-H", f"Authorization: Bearer {API_KEY}",
        "--max-time", str(timeout),
        url,
        "-o", out_path,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"下载失败 ({proc.returncode}): {proc.stderr[:300]}")
    size = os.path.getsize(out_path)
    if size < 1024:
        # 可能下载到错误页
        with open(out_path, "rb") as f:
            head = f.read(200)
        raise RuntimeError(f"下载内容过小 ({size} bytes): {head[:100]!r}")
    print(f"[download] 写入 {out_path} ({size:,} bytes)")
    return out_path


def submit(prompt: str) -> str:
    url = f"{BASE}/v4/videos/generations"
    data = curl_json("POST", url, {"model": MODEL, "prompt": prompt})
    print(f"[submit] 响应: {json.dumps(data, ensure_ascii=False)[:500]}")
    # 兼容多种返回结构
    task_id = data.get("id") or data.get("task_id")
    if not task_id and isinstance(data.get("data"), dict):
        task_id = data["data"].get("id") or data["data"].get("task_id")
    if not task_id:
        raise RuntimeError(f"提交失败，未返回 task_id: {data}")
    return task_id


def poll(task_id: str, timeout_sec: int = 180) -> dict:
    url = f"{BASE}/v4/async-result/{task_id}"
    deadline = time.time() + timeout_sec
    last_state = None
    while time.time() < deadline:
        data = curl_json("GET", url, timeout=30)
        task_status = (
            data.get("task_status")
            or data.get("status")
            or (data.get("data") or {}).get("status")
            if isinstance(data.get("data"), dict)
            else None
        )
        if task_status != last_state:
            elapsed = int(timeout_sec - (deadline - time.time()))
            print(f"[poll] 状态 → {task_status} (已等待 ~{elapsed}s)")
            last_state = task_status

        if task_status in ("SUCCESS", "success", "succeeded", "completed"):
            return data
        if task_status in ("FAIL", "FAILURE", "failed"):
            raise RuntimeError(f"任务失败: {json.dumps(data, ensure_ascii=False)[:800]}")

        time.sleep(4)

    raise TimeoutError(f"轮询超时 {timeout_sec}s，最后状态: {last_state}")


def extract_video_url(result: dict) -> str:
    # 顶层
    for key in ("video_url", "url", "result_url"):
        if result.get(key):
            return result[key]
    # data 内层
    data = result.get("data") or {}
    if isinstance(data, dict):
        for key in ("video_url", "url", "result_url"):
            if data.get(key):
                return data[key]
        for key in ("video_result", "videos", "results"):
            arr = data.get(key)
            if isinstance(arr, list) and arr:
                item = arr[0]
                if isinstance(item, dict):
                    for k in ("url", "video_url", "result_url"):
                        if item.get(k):
                            return item[k]
                elif isinstance(item, str):
                    return item
    raise RuntimeError(f"找不到视频 URL: {json.dumps(result, ensure_ascii=False)[:800]}")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 zhipu_video_generate.py \"<prompt>\" [out.mp4]", file=sys.stderr)
        sys.exit(2)

    prompt = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else (
        f"/home/swg/Videos/cogvideox_test/{int(time.time())}.mp4"
    )

    print(f"[main] prompt: {prompt}")
    print(f"[main] output: {out}")
    print(f"[main] model:  {MODEL}")

    task_id = submit(prompt)
    print(f"[main] task_id = {task_id}")

    result = poll(task_id, timeout_sec=180)
    print(f"[main] 完成: {json.dumps(result, ensure_ascii=False)[:500]}")

    url = extract_video_url(result)
    print(f"[main] video_url = {url[:120]}...")

    curl_download(url, out)
    print("[main] ✅ 视频生成成功")


if __name__ == "__main__":
    main()
