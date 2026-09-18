/* ===== AI 工具导航站 app.js ===== */
(function () {
  "use strict";

  /* ---------- 主题切换 ---------- */
  var themeBtn = document.getElementById("themeToggle");
  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    if (themeBtn) themeBtn.textContent = t === "dark" ? "☀️" : "🌙";
  }
  var saved = null;
  try { saved = localStorage.getItem("theme"); } catch (e) {}
  applyTheme(saved || (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  /* ---------- 年份 ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- 站内搜索 ---------- */
  var ROOT = document.body.getAttribute("data-root") || "";
  var INDEX = [
    { name: "ChatGPT", cat: "AI 写作 / AI 聊天", href: "tool/chatgpt.html" },
    { name: "Claude", cat: "AI 写作 / AI 聊天", href: "tool/claude.html" },
    { name: "Gemini", cat: "AI 聊天", href: "tool/gemini.html" },
    { name: "Jasper", cat: "AI 写作", href: "tool/jasper.html" },
    { name: "Copy.ai", cat: "AI 写作", href: "tool/copyai.html" },
    { name: "Notion AI", cat: "AI 办公", href: "tool/notion-ai.html" },
    { name: "Midjourney", cat: "AI 绘画", href: "tool/midjourney.html" },
    { name: "DALL·E 3", cat: "AI 绘画", href: "tool/dalle3.html" },
    { name: "Runway", cat: "AI 视频", href: "tool/runway.html" },
    { name: "Suno", cat: "AI 音频/音乐", href: "tool/suno.html" },
    { name: "ElevenLabs", cat: "AI 音频/音乐", href: "tool/elevenlabs.html" },
    { name: "GitHub Copilot", cat: "AI 编程", href: "tool/github-copilot.html" },
    { name: "Cursor", cat: "AI 编程", href: "tool/cursor.html" },
    { name: "Perplexity", cat: "AI 搜索", href: "tool/perplexity.html" },
    { name: "DeepL", cat: "AI 翻译", href: "tool/deepl.html" },
    { name: "AI 写作分类", cat: "分类", href: "category/ai-writing.html" },
    { name: "AI 绘画分类", cat: "分类", href: "category/ai-art.html" },
    { name: "AI 视频分类", cat: "分类", href: "category/ai-video.html" },
    { name: "AI 音频分类", cat: "分类", href: "category/ai-audio.html" },
    { name: "AI 编程分类", cat: "分类", href: "category/ai-code.html" },
    { name: "AI 聊天分类", cat: "分类", href: "category/ai-chat.html" },
    { name: "AI 设计分类", cat: "分类", href: "category/ai-design.html" },
    { name: "AI 办公分类", cat: "分类", href: "category/ai-office.html" },
    { name: "AI 搜索分类", cat: "分类", href: "category/ai-search.html" },
    { name: "AI 翻译分类", cat: "分类", href: "category/ai-translate.html" },
    { name: "AI 数据分析分类", cat: "分类", href: "category/ai-data.html" },
    { name: "AI 营销分类", cat: "分类", href: "category/ai-marketing.html" },
    { name: "AI 学习分类", cat: "分类", href: "category/ai-learning.html" },
    { name: "AI 客服分类", cat: "分类", href: "category/ai-service.html" },
    { name: "AI 开源工具分类", cat: "分类", href: "category/ai-opensource.html" }
  ];

  var inputs = document.querySelectorAll("#globalSearch");
  inputs.forEach(function (input) {
    var box = input.closest(".search-box");
    var results = box ? box.querySelector(".search-results") : null;
    if (!results) return;

    function render(q) {
      q = q.trim().toLowerCase();
      if (!q) { results.classList.remove("show"); results.innerHTML = ""; return; }
      var hits = INDEX.filter(function (x) {
        return x.name.toLowerCase().indexOf(q) > -1 || x.cat.toLowerCase().indexOf(q) > -1;
      }).slice(0, 8);
      if (!hits.length) {
        results.innerHTML = '<div class="search-empty">未找到相关工具，试试 "ChatGPT" 或 "绘画"</div>';
      } else {
        results.innerHTML = hits.map(function (x) {
          return '<a href="' + ROOT + x.href + '"><span>' + x.name + "</span><span class=\"sr-cat\">" + x.cat + "</span></a>";
        }).join("");
      }
      results.classList.add("show");
    }

    input.addEventListener("input", function () { render(input.value); });
    input.addEventListener("focus", function () { if (input.value.trim()) render(input.value); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { results.classList.remove("show"); input.blur(); }
      if (e.key === "Enter") {
        var first = results.querySelector("a");
        if (first) window.location.href = first.getAttribute("href");
      }
    });
    document.addEventListener("click", function (e) {
      if (!box.contains(e.target)) results.classList.remove("show");
    });
  });

  /* ---------- 分类页：加载更多 ---------- */
  var loadBtn = document.getElementById("loadMoreBtn");
  if (loadBtn) {
    loadBtn.addEventListener("click", function () {
      var more = document.querySelector(".more-tools");
      if (more) more.hidden = false;
      loadBtn.parentElement.remove();
    });
  }
})();
