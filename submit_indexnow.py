# -*- coding: utf-8 -*-
"""向 IndexNow (Bing/Yandex等) 批量提交全站网址"""
import json
import urllib.request

KEY = "d8c0e09072f1cda03f43e2e639f386af"
BASE = "https://211014049.github.io/ai-tools"

cats = ("ai-writing ai-art ai-video ai-audio ai-code ai-chat ai-design ai-office "
        "ai-search ai-translate ai-data ai-marketing ai-learning ai-service ai-opensource").split()
tools = ("chatgpt claude jasper copyai midjourney dalle3 runway suno elevenlabs "
         "github-copilot gemini perplexity notion-ai cursor deepl").split()

paths = ["", "index.html"] + [f"category/{s}.html" for s in cats] \
        + [f"tool/{s}.html" for s in tools] \
        + ["privacy-policy.html", "about.html", "contact.html"]
urls = [f"{BASE}/{p}" if p else BASE + "/" for p in paths]

payload = {"host": "211014049.github.io", "key": KEY, "urlList": urls}
req = urllib.request.Request("https://api.indexnow.org/indexnow",
                             data=json.dumps(payload).encode(),
                             headers={"Content-Type": "application/json; charset=utf-8"})
proxy = urllib.request.ProxyHandler({"https": "http://127.0.0.1:7890", "http": "http://127.0.0.1:7890"})
opener = urllib.request.build_opener(proxy)
try:
    r = opener.open(req, timeout=25)
    print("IndexNow 提交成功 ->", r.status, r.read().decode()[:200])
    print(f"已提交 {len(urls)} 个网址")
except Exception as e:
    print("IndexNow 提交失败:", e)
