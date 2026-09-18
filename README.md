# AI 工具导航站

纯静态 AI 工具导航网站，托管在 GitHub Pages 上即可运行，无需后端。

## 网站内容

- 34 个 HTML 页面：首页 1 + 分类页 15 + 工具详情页 15 + 政策页 3
- 收录 64 个 AI 工具（去重统计）
- 每页含独立 SEO 标签（title / description / Open Graph / canonical）
- JSON-LD 结构化数据：WebSite、BreadcrumbList、SoftwareApplication、FAQPage
- sitemap.xml + robots.txt 已生成
- 预留 Google AdSense 广告位（顶部 banner + 侧边栏，见页面内注释）
- 外链统一 `rel="nofollow noopener" target="_blank"`

## 上传到 GitHub Pages（3 步）

1. 在 GitHub 新建一个**空**仓库（不要勾选 README），例如 `ai-tools`
2. 在本目录（ai-tools-site）执行：

```bash
git remote add origin https://github.com/你的用户名/ai-tools.git
git push -u origin main
```

3. 仓库 Settings → Pages → Branch 选 `main` / `/(root)` → Save

稍等 1-2 分钟，访问 `https://你的用户名.github.io/ai-tools/` 即可。

> 上传前记得把 `generate.py` 第 17 行的 `SITE_URL` 改成上面的真实地址，
> 然后运行 `python generate.py` 重新生成一次，再 push。

## 本地预览

直接双击 `docs/index.html` 即可在浏览器打开，所有链接为相对路径。

## 修改与扩展

- 所有数据集中在 `generate.py`：
  - `TOOLS`：工具详情页数据（要加新工具详情页，往这里加条目即可）
  - `CATEGORIES` / `CATEGORY_TOOLS`：分类与其收录的工具
  - `SITE_URL`：上线域名
- 修改后运行 `python generate.py` 重新生成全站

## 待办（上线后）

- [ ] 替换联盟链接（各工具 `affiliate` 字段）
- [ ] 申请并接入 Google AdSense（替换页面内广告占位块）
- [ ] 提交 sitemap 到 Google Search Console / Bing 站长平台
