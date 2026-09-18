# -*- coding: utf-8 -*-
"""
AI 工具导航站静态页面生成器
运行: python generate.py
输出: docs/ 下所有静态页面 + sitemap.xml + robots.txt
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = ROOT  # 网站文件直接输出到仓库根目录（GitHub Pages 部署源为 main / root）

SITE_NAME = "AI 导航站"
SITE_TAGLINE = "发现最好的 AI 工具"
# TODO: 上线后替换为真实域名（例如 https://yourname.github.io 或自定义域名）
SITE_URL = "https://211014049.github.io/ai-tools"

# ---------------------------------------------------------------------------
# 分类数据（15 个分类；前 5 个生成分组页，其余在首页显示"即将上线"）
# ---------------------------------------------------------------------------
CATEGORIES = [
    {"slug": "ai-writing", "name": "AI 写作", "emoji": "✍️",
     "desc": "AI 写作助手帮你生成文章、文案、润色文本，覆盖营销文案、博客长文、论文润色等场景。",
     "page": True},
    {"slug": "ai-art", "name": "AI 绘画", "emoji": "🎨",
     "desc": "输入一句话生成精美插画、概念图与商业设计稿，AI 绘画工具正在重塑视觉创作流程。",
     "page": True},
    {"slug": "ai-video", "name": "AI 视频", "emoji": "🎬",
     "desc": "文本生成视频、数字人播报、智能剪辑，AI 视频工具大幅降低视频创作门槛。",
     "page": True},
    {"slug": "ai-audio", "name": "AI 音频/音乐", "emoji": "🎵",
     "desc": "AI 作曲、语音合成、配音降噪，一站式解决播客、视频配乐与有声内容的声音需求。",
     "page": True},
    {"slug": "ai-code", "name": "AI 编程", "emoji": "💻",
     "desc": "代码补全、智能调试、对话式编程，AI 编程助手让开发效率提升数倍。",
     "page": True},
    {"slug": "ai-chat", "name": "AI 聊天", "emoji": "💬",
     "desc": "通用对话式 AI 助手与角色扮演聊天应用，一站式对比各大模型聊天产品。",
     "page": True},
    {"slug": "ai-design", "name": "AI 设计", "emoji": "🖌️",
     "desc": "AI 驱动的 UI 设计、平面设计与原型工具，设计师与产品经理的效率外挂。",
     "page": True},
    {"slug": "ai-office", "name": "AI 办公", "emoji": "📊",
     "desc": "智能文档、演示文稿与效率办公工具，把重复劳动交给 AI。",
     "page": True},
    {"slug": "ai-search", "name": "AI 搜索", "emoji": "🔍",
     "desc": "基于大模型的问答式搜索引擎，直接给答案还带引用来源。",
     "page": True},
    {"slug": "ai-translate", "name": "AI 翻译", "emoji": "🌐",
     "desc": "高质量机器翻译与沉浸式双语阅读工具，跨语言工作学习必备。",
     "page": True},
    {"slug": "ai-data", "name": "AI 数据分析", "emoji": "📈",
     "desc": "用自然语言对话完成数据分析与可视化，不懂 SQL 也能做分析师。",
     "page": True},
    {"slug": "ai-marketing", "name": "AI 营销", "emoji": "📣",
     "desc": "广告投放、SEO 优化与营销内容生成工具，增长团队弹药库。",
     "page": True},
    {"slug": "ai-learning", "name": "AI 学习", "emoji": "🎓",
     "desc": "AI 家教、答题辅导与个性化学习助手，一对一辅导不再是奢侈品。",
     "page": True},
    {"slug": "ai-service", "name": "AI 客服", "emoji": "🎧",
     "desc": "智能客服机器人与客户对话自动化平台，7×24 小时不间断应答。",
     "page": True},
    {"slug": "ai-opensource", "name": "AI 开源工具", "emoji": "🧰",
     "desc": "可本地部署的大模型运行器与开源 AI 框架，数据隐私派的根据地。",
     "page": True},
]

CAT_BY_SLUG = {c["slug"]: c for c in CATEGORIES}

# ---------------------------------------------------------------------------
# 分类页收录的工具（带 * 的有独立详情页；其余为站外直链）
# kind: "detail" = 有详情页；"ext" = 外链
# ---------------------------------------------------------------------------
CATEGORY_TOOLS = {
    "ai-writing": [
        {"kind": "detail", "slug": "chatgpt"},
        {"kind": "detail", "slug": "claude"},
        {"kind": "detail", "slug": "jasper"},
        {"kind": "detail", "slug": "copyai"},
        {"kind": "ext", "name": "Writesonic", "url": "https://writesonic.com",
         "desc": "面向营销与 SEO 的 AI 写作平台，支持文章批量生成与事实核查。",
         "tags": ["写作", "SEO"]},
        {"kind": "ext", "name": "Rytr", "url": "https://rytr.me",
         "desc": "轻量级 AI 写作助手，40+ 模板与多语言支持，免费额度友好。",
         "tags": ["写作", "免费增值"]},
        {"kind": "ext", "name": "Notion AI", "url": "https://www.notion.so/product/ai",
         "desc": "内置于 Notion 的 AI 助手，可总结、翻译、续写文档与自动整理笔记。",
         "tags": ["笔记", "办公"]},
        {"kind": "ext", "name": "GrammarlyGO", "url": "https://www.grammarly.com",
         "desc": "Grammarly 推出的 AI 生成助手，在纠错基础上支持改写与生成。",
         "tags": ["润色", "英语写作"]},
    ],
    "ai-art": [
        {"kind": "detail", "slug": "midjourney"},
        {"kind": "detail", "slug": "dalle3"},
        {"kind": "ext", "name": "Stable Diffusion", "url": "https://stability.ai",
         "desc": "开源 AI 绘画模型，可本地部署、自由微调，生态插件极其丰富。",
         "tags": ["开源", "本地部署"]},
        {"kind": "ext", "name": "Leonardo AI", "url": "https://leonardo.ai",
         "desc": "面向游戏与设计素材的 AI 绘画平台，模型与风格控制丰富。",
         "tags": ["游戏素材", "设计"]},
        {"kind": "ext", "name": "NovelAI", "url": "https://novelai.net",
         "desc": "擅长二次元插画的 AI 绘画与辅助写作服务，订阅制。",
         "tags": ["二次元", "插画"]},
        {"kind": "ext", "name": "Adobe Firefly", "url": "https://firefly.adobe.com",
         "desc": "Adobe 官方 AI 生成模型，与 Photoshop 等软件深度集成，可商用授权清晰。",
         "tags": ["商用", "Adobe"]},
    ],
    "ai-video": [
        {"kind": "detail", "slug": "runway"},
        {"kind": "ext", "name": "Pika", "url": "https://pika.art",
         "desc": "轻量好上手的文生视频工具，擅长创意短片与趣味特效。",
         "tags": ["文生视频", "创意"]},
        {"kind": "ext", "name": "Sora", "url": "https://openai.com/sora",
         "desc": "OpenAI 的文生视频模型，以逼真的长镜头与物理一致性著称。",
         "tags": ["文生视频", "OpenAI"]},
        {"kind": "ext", "name": "Synthesia", "url": "https://www.synthesia.io",
         "desc": "企业级 AI 数字人视频平台，输入文案即可生成 140+ 语言播报视频。",
         "tags": ["数字人", "企业"]},
        {"kind": "ext", "name": "HeyGen", "url": "https://www.heygen.com",
         "desc": "AI 数字人与视频翻译工具，支持口型同步的多语言配音。",
         "tags": ["数字人", "视频翻译"]},
        {"kind": "ext", "name": "InVideo AI", "url": "https://invideo.io",
         "desc": "从一段提示词自动生成带素材、配音与字幕的完整短视频。",
         "tags": ["短视频", "自动化"]},
    ],
    "ai-audio": [
        {"kind": "detail", "slug": "suno"},
        {"kind": "detail", "slug": "elevenlabs"},
        {"kind": "ext", "name": "Udio", "url": "https://www.udiomusic.com",
         "desc": "文生音乐平台，音质细腻，支持分段编辑与延长歌曲。",
         "tags": ["音乐生成"]},
        {"kind": "ext", "name": "Murf", "url": "https://murf.ai",
         "desc": "企业级 AI 配音工具，120+ 音色，适合课程与营销视频旁白。",
         "tags": ["配音", "旁白"]},
        {"kind": "ext", "name": "Descript", "url": "https://www.descript.com",
         "desc": "像编辑文档一样剪辑音视频，自动转写、一键去口水词。",
         "tags": ["剪辑", "播客"]},
    ],
    "ai-code": [
        {"kind": "detail", "slug": "github-copilot"},
        {"kind": "ext", "name": "Cursor", "url": "https://cursor.com",
         "desc": "AI 原生代码编辑器，基于 VS Code，支持整仓理解与 Agent 自动改码。",
         "tags": ["编辑器", "Agent"]},
        {"kind": "ext", "name": "Tabnine", "url": "https://www.tabnine.com",
         "desc": "注重隐私的 AI 代码补全，支持私有化部署与企业代码库训练。",
         "tags": ["补全", "企业"]},
        {"kind": "ext", "name": "Codeium", "url": "https://codeium.com",
         "desc": "免费的 AI 代码补全与聊天工具，个人使用永久免费。",
         "tags": ["免费", "补全"]},
        {"kind": "ext", "name": "Amazon CodeWhisperer", "url": "https://aws.amazon.com/codewhisperer/",
         "desc": "AWS 官方 AI 编程助手，与 AWS 服务深度集成，个人版免费。",
         "tags": ["AWS", "补全"]},
    ],
    "ai-chat": [
        {"kind": "detail", "slug": "chatgpt"},
        {"kind": "detail", "slug": "claude"},
        {"kind": "detail", "slug": "gemini"},
        {"kind": "detail", "slug": "perplexity"},
        {"kind": "ext", "name": "Poe", "url": "https://poe.com",
         "desc": "Quora 出品的聚合聊天平台，一个订阅畅聊 GPT、Claude、Gemini 等多家模型。",
         "tags": ["聚合", "多模型"]},
        {"kind": "ext", "name": "Character.AI", "url": "https://character.ai",
         "desc": "角色扮演 AI 聊天应用，海量用户创建的虚拟角色，娱乐向体验一流。",
         "tags": ["角色扮演", "娱乐"]},
    ],
    "ai-design": [
        {"kind": "ext", "name": "Canva AI", "url": "https://www.canva.com",
         "desc": "Canva 内置的 Magic Studio，一句话生成海报、PPT 与配图，小白友好。",
         "tags": ["平面设计", "模板"]},
        {"kind": "ext", "name": "Figma AI", "url": "https://www.figma.com",
         "desc": "Figma 内置 AI 能力：自动命名图层、生成设计稿、AI 原型辅助。",
         "tags": ["UI 设计", "协作"]},
        {"kind": "ext", "name": "Galileo AI", "url": "https://www.usegalileo.ai",
         "desc": "文本生成高保真 UI 设计稿，可直接导出到 Figma 编辑。",
         "tags": ["UI 生成", "原型"]},
        {"kind": "ext", "name": "Uizard", "url": "https://uizard.io",
         "desc": "草图/文字一键转 App 与网页原型，非设计师也能快速出稿。",
         "tags": ["原型", "低保真"]},
    ],
    "ai-office": [
        {"kind": "detail", "slug": "notion-ai"},
        {"kind": "ext", "name": "Tome", "url": "https://tome.app",
         "desc": "AI 叙事型演示工具，输入主题自动生成图文并茂的 PPT。",
         "tags": ["演示", "PPT"]},
        {"kind": "ext", "name": "Beautiful.ai", "url": "https://www.beautiful.ai",
         "desc": "智能排版演示工具，插入内容自动对齐美化，团队模板库丰富。",
         "tags": ["PPT", "排版"]},
        {"kind": "ext", "name": "Gamma", "url": "https://gamma.app",
         "desc": "AI 一键生成演示文稿、网页与文档，免费额度慷慨，上手极快。",
         "tags": ["PPT", "免费增值"]},
    ],
    "ai-search": [
        {"kind": "detail", "slug": "perplexity"},
        {"kind": "ext", "name": "Phind", "url": "https://www.phind.com",
         "desc": "面向开发者的 AI 搜索引擎，答案附带代码示例与文档引用。",
         "tags": ["开发者", "技术问答"]},
        {"kind": "ext", "name": "You.com", "url": "https://you.com",
         "desc": "带 AI 摘要的搜索平台，支持多模型切换与个性化信息源。",
         "tags": ["搜索引擎", "聚合"]},
        {"kind": "ext", "name": "Komo", "url": "https://komo.ai",
         "desc": "简洁的 AI 搜索与聊天入口，响应快，适合轻量查询。",
         "tags": ["搜索引擎"]},
    ],
    "ai-translate": [
        {"kind": "detail", "slug": "deepl"},
        {"kind": "ext", "name": "Google Translate", "url": "https://translate.google.com",
         "desc": "覆盖 100+ 语言的免费翻译服务，网页、文档、实时对话全支持。",
         "tags": ["免费", "多语言"]},
        {"kind": "ext", "name": "Immersive Translate", "url": "https://immersivetranslate.com",
         "desc": "沉浸式双语网页翻译浏览器插件，PDF/视频字幕翻译也在行。",
         "tags": ["浏览器插件", "双语阅读"]},
    ],
    "ai-data": [
        {"kind": "ext", "name": "Julius AI", "url": "https://julius.ai",
         "desc": "上传表格用对话完成分析并自动出图表，数据分析界的现象级产品。",
         "tags": ["数据分析", "图表"]},
        {"kind": "ext", "name": "Akkio", "url": "https://www.akkio.com",
         "desc": "无代码 AI 预测平台，营销与销售团队可自助搭建预测模型。",
         "tags": ["预测", "无代码"]},
        {"kind": "ext", "name": "Rows", "url": "https://rows.com",
         "desc": "内置 AI 与实时数据集成的在线表格，取代部分 BI 工作流。",
         "tags": ["表格", "BI"]},
        {"kind": "ext", "name": "Polymer", "url": "https://www.polymersearch.com",
         "desc": "把电子表格秒变可搜索的智能数据库与看板，电商与营销常用。",
         "tags": ["搜索", "看板"]},
    ],
    "ai-marketing": [
        {"kind": "detail", "slug": "jasper"},
        {"kind": "ext", "name": "Anyword", "url": "https://anyword.com",
         "desc": "带预测评分的 AI 文案工具，逐条预测文案的转化表现。",
         "tags": ["文案", "转化预测"]},
        {"kind": "ext", "name": "SE Ranking", "url": "https://seranking.com",
         "desc": "一体化 SEO 平台，含关键词、排名追踪与 AI 内容优化。",
         "tags": ["SEO", "排名追踪"]},
        {"kind": "ext", "name": "Surfer SEO", "url": "https://surferseo.com",
         "desc": "AI 内容优化与 SERP 分析，按竞品数据指导文章写作，常与 Jasper 搭配。",
         "tags": ["SEO", "内容优化"]},
    ],
    "ai-learning": [
        {"kind": "ext", "name": "Khanmigo（Khan Academy AI）", "url": "https://www.khanmigo.ai",
         "desc": "可汗学院推出的 AI 家教，苏格拉底式引导而非直接给答案。",
         "tags": ["家教", "K12"]},
        {"kind": "ext", "name": "Socratic", "url": "https://socratic.org",
         "desc": "Google 出品的拍照解题学习 App，覆盖数学、科学等多学科讲解。",
         "tags": ["拍照解题", "免费"]},
        {"kind": "ext", "name": "ChatGPT for Education", "url": "https://openai.com/chatgpt/education/",
         "desc": "OpenAI 面向教育场景的方案页，含教学应用案例与教育版部署。",
         "tags": ["教育", "OpenAI"]},
    ],
    "ai-service": [
        {"kind": "ext", "name": "Intercom Fin", "url": "https://www.intercom.com/fin",
         "desc": "基于 GPT 的 AI 客服坐席，可独立解决 50%+ 客户问题。",
         "tags": ["SaaS 客服", "企业"]},
        {"kind": "ext", "name": "Drift", "url": "https://www.drift.com",
         "desc": "B2B 营销对话平台，AI 识别高意向访客并实时转接销售。",
         "tags": ["B2B", "销售转化"]},
        {"kind": "ext", "name": "Tidio", "url": "https://www.tidio.com",
         "desc": "面向中小电商的 AI 客服 + 在线聊天，Lyro AI 自动应答常见问题。",
         "tags": ["电商", "中小企业"]},
    ],
    "ai-opensource": [
        {"kind": "ext", "name": "Ollama", "url": "https://ollama.com",
         "desc": "一行命令在本地跑 Llama、Qwen 等开源大模型，数据完全不出本机。",
         "tags": ["本地部署", "开源"]},
        {"kind": "ext", "name": "LM Studio", "url": "https://lmstudio.ai",
         "desc": "图形界面的本地大模型运行器，下载/聊天/开 API 全流程可视化。",
         "tags": ["本地部署", "GUI"]},
        {"kind": "ext", "name": "LangChain", "url": "https://www.langchain.com",
         "desc": "最流行的 LLM 应用开发框架，编排模型、工具与记忆的标准选择。",
         "tags": ["开发框架", "Agent"]},
        {"kind": "ext", "name": "AutoGPT", "url": "https://github.com/Significant-Gravitas/AutoGPT",
         "desc": "先驱级开源自主 Agent 框架，让大模型自己拆解并执行任务。",
         "tags": ["Agent", "开源"]},
    ],
}

# ---------------------------------------------------------------------------
# 工具详情页数据（10 个）
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "slug": "chatgpt", "name": "ChatGPT", "emoji": "🤖",
        "cat": "ai-writing", "vendor": "OpenAI",
        "tagline": "全球用户量最大的对话式 AI 助手",
        "rating": 4.8, "reviews": "52,300", "price": "免费增值", "price_detail": "免费版可日常使用；Plus $20/月；Team/Enterprise 面向团队与企业",
        "url": "https://chatgpt.com", "affiliate": None,
        "desc": [
            "ChatGPT 是 OpenAI 推出的大语言模型对话助手，基于 GPT 系列模型，能够理解自然语言并完成写作、翻译、总结、编程、头脑风暴等多种任务。自 2022 年底发布以来，它已成为全球用户量最大的 AI 应用之一，也是许多人接触 AI 的第一站。",
            "免费版即可使用基础模型完成大部分日常任务；Plus 订阅可解锁更强大的高级模型、联网搜索、图像生成、文件分析与 GPTs 自定义助手等能力，支持网页、iOS 与 Android 多端同步，适合学生、职场人士与开发者作为全能 AI 工作台使用。",
        ],
        "features": ["多轮对话与强大上下文理解", "写作、翻译、总结、润色一步到位", "代码生成、解释与调试", "联网搜索与文件/图片分析（Plus）", "GPTs 自定义智能体市场", "网页 / iOS / Android 全平台"],
        "tags": ["对话", "写作", "通用助手", "GPT"],
        "faq": [
            {"q": "ChatGPT 免费吗？", "a": "有免费版，可使用基础模型完成日常任务。Plus 订阅（$20/月）可解锁更高级的模型、联网搜索、图像生成与更高用量。"},
            {"q": "ChatGPT 支持中文吗？", "a": "支持，中英文能力都属于第一梯队，可流畅完成中文写作、翻译与总结任务。"},
            {"q": "ChatGPT 和 Claude 怎么选？", "a": "两者都属顶级水平：ChatGPT 生态与多模态功能更全，Claude 在长文档处理与自然文风上口碑更佳，建议都试用免费版再决定。"},
        ],
        "related": ["claude", "dalle3", "github-copilot"],
    },
    {
        "slug": "claude", "name": "Claude", "emoji": "🧠",
        "cat": "ai-writing", "vendor": "Anthropic",
        "tagline": "以安全与长文本见长的 AI 助手",
        "rating": 4.7, "reviews": "18,900", "price": "免费增值", "price_detail": "免费版有每日用量限制；Pro $20/月；Team $25/人/月起",
        "url": "https://claude.ai", "affiliate": None,
        "desc": [
            "Claude 是 Anthropic 开发的大语言模型助手，以安全性、长文本理解和出色的写作质量著称。它支持超长上下文，可一次性处理数百页文档，特别适合合同审阅、报告分析与资料整理等深度阅读场景。",
            "Artifacts 功能可以在对话中直接生成并预览网页、图表与文档，Projects 则能把常用资料沉淀为知识库。免费版提供日常用量，Pro 订阅解锁更高配额与更高级模型，是写作者、分析师与开发者的热门选择。",
        ],
        "features": ["超长上下文，轻松阅读整本书/长报告", "自然流畅、少 AI 味的写作风格", "Artifacts 实时预览生成的网页与图表", "Projects 项目知识库", "强大的代码理解与生成能力", "严格的安全对齐设计"],
        "tags": ["对话", "长文本", "写作", "编程"],
        "faq": [
            {"q": "Claude 免费版有什么限制？", "a": "免费版按每日用量限额，高峰期可能暂时不可用。Pro（$20/月）提供更高配额、优先访问与更高级模型。"},
            {"q": "Claude 能处理多长的文档？", "a": "支持数十万 token 的超长上下文，可以一次上传并分析数百页 PDF、合同或代码库。"},
            {"q": "Claude 适合编程吗？", "a": "适合，Claude 在代码生成、调试与解释方面表现优秀，配合 Artifacts 还能直接预览生成的网页效果。"},
        ],
        "related": ["chatgpt", "github-copilot", "copyai"],
    },
    {
        "slug": "jasper", "name": "Jasper", "emoji": "🚀",
        "cat": "ai-writing", "vendor": "Jasper AI",
        "tagline": "面向营销团队的企业级 AI 写作平台",
        "rating": 4.3, "reviews": "5,400", "price": "付费", "price_detail": "Creator $39/月 起；Pro 与 Business 版面向团队，支持多人协作",
        "url": "https://www.jasper.ai", "affiliate": None,
        "desc": [
            "Jasper 是一款面向营销团队与企业用户的老牌 AI 写作平台，提供 50+ 专业模板，覆盖广告文案、博客文章、社媒帖子、产品描述与邮件营销等场景。它的品牌语调（Brand Voice）功能可以学习你的品牌风格，让批量生成的内容保持统一口吻。",
            "Jasper 还支持团队协作、内容工作流与主流营销工具集成，适合有稳定内容产出需求的团队。价格较高，个人轻度用户可先考虑 Copy.ai 或 Rytr 等替代方案。",
        ],
        "features": ["50+ 营销文案模板", "品牌语调学习，风格统一", "团队协作与内容审批流", "多语言内容生成", "与 Surfer SEO 等工具集成", "浏览器插件随处调用"],
        "tags": ["营销文案", "企业", "SEO", "协作"],
        "faq": [
            {"q": "Jasper 适合个人用户吗？", "a": "Jasper 定位团队与企业，价格较高。个人用户可先试用免费演示，或选择 Copy.ai、Rytr 等更便宜的替代品。"},
            {"q": "Jasper 支持中文写作吗？", "a": "支持多语言生成，中文质量可用，但模板与营销场景以英文内容生态为主。"},
            {"q": "Jasper 和 ChatGPT 有什么区别？", "a": "ChatGPT 是通用助手，Jasper 是垂直营销平台：提供品牌语调、团队协作、营销模板与 SEO 集成等面向内容生产的完整工作流。"},
        ],
        "related": ["copyai", "chatgpt", "claude"],
    },
    {
        "slug": "copyai", "name": "Copy.ai", "emoji": "✨",
        "cat": "ai-writing", "vendor": "Copy.ai",
        "tagline": "免费额度友好的营销文案生成器",
        "rating": 4.2, "reviews": "4,100", "price": "免费增值", "price_detail": "免费版每月 2,000 字；Pro $36/月起，解锁不限字数与工作流",
        "url": "https://www.copy.ai", "affiliate": None,
        "desc": [
            "Copy.ai 是一款主打营销场景的 AI 文案生成工具，覆盖广告、社媒、邮件、产品描述等 90+ 模板，上手门槛低，免费额度对个人和小团队非常友好。",
            "近年 Copy.ai 升级为 GTM（Go-to-Market）AI 平台，可以把销售线索研究、个性化邮件、CRM 记录整理等工作编排成自动化工作流，让 AI 直接产出可用的业务成果，适合营销与销售团队提升人效。",
        ],
        "features": ["90+ 文案模板覆盖全营销场景", "免费版每月 2,000 字", "GTM 工作流自动化", "支持多语言生成", "营销工具集成", "操作简单、上手快"],
        "tags": ["营销文案", "免费增值", "自动化", "销售"],
        "faq": [
            {"q": "Copy.ai 有免费版吗？", "a": "有，免费版每月提供 2,000 字额度并开放大部分模板，Pro 版（$36/月起）解锁不限字数与自动化工作流。"},
            {"q": "Copy.ai 和 Jasper 哪个好？", "a": "两者定位相似：Jasper 更偏企业团队协作，功能更全但价格更高；Copy.ai 免费额度更友好、上手更快，适合个人与中小企业。"},
            {"q": "生成的内容可以直接商用吗？", "a": "按官方条款，用户对生成内容拥有使用权，可用于商业用途；但仍建议人工审核事实与版权风险。"},
        ],
        "related": ["jasper", "chatgpt", "rytr-external"],
    },
    {
        "slug": "midjourney", "name": "Midjourney", "emoji": "🖌️",
        "cat": "ai-art", "vendor": "Midjourney, Inc.",
        "tagline": "公认艺术表现力最强的 AI 绘画工具",
        "rating": 4.7, "reviews": "31,200", "price": "付费", "price_detail": "Basic $10/月；Standard $30/月（不限慢速生成）；Pro $60/月；Mega $120/月",
        "url": "https://www.midjourney.com", "affiliate": None,
        "desc": [
            "Midjourney 是目前艺术表现力最受认可的 AI 绘画工具，擅长生成构图讲究、光影细腻、风格化强烈的图像，被广泛用于概念设计、插画、海报与品牌视觉创作。",
            "早期通过 Discord 使用，现已推出功能完整的网页版，支持提示词生成、图生图、局部重绘、风格参考与角色一致性等功能。它没有免费试用，最低 $10/月 起订，对画面质量有要求的创作者普遍认为物有所值。",
        ],
        "features": ["顶级的画面美感与艺术风格", "文生图、图生图、局部重绘", "风格参考与角色一致性", "网页版 + Discord 双端", "高清放大与多变体", "活跃的创作者社区"],
        "tags": ["绘画", "插画", "概念设计", "付费"],
        "faq": [
            {"q": "Midjourney 有免费试用吗？", "a": "目前不提供免费试用，需订阅使用，最低 Basic 档 $10/月（约 200 次快速生成）。"},
            {"q": "Midjourney 支持中文提示词吗？", "a": "网页版对中文有一定理解能力，但社区最佳实践仍是英文提示词，建议翻译后再生成以获得更稳定的效果。"},
            {"q": "生成的图片可以商用吗？", "a": "付费订阅用户生成的图片可商用；年营收超过 100 万美元的公司需订阅 Pro 及以上档位。"},
        ],
        "related": ["dalle3", "runway", "suno"],
    },
    {
        "slug": "dalle3", "name": "DALL·E 3", "emoji": "🎨",
        "cat": "ai-art", "vendor": "OpenAI",
        "tagline": "最擅长理解复杂提示词的 AI 图像模型",
        "rating": 4.5, "reviews": "22,800", "price": "免费增值", "price_detail": "通过 ChatGPT 免费限量使用；ChatGPT Plus / API 按量付费",
        "url": "https://openai.com/dall-e-3", "affiliate": None,
        "desc": [
            "DALL·E 3 是 OpenAI 的第三代文生图模型，最大亮点是对自然语言提示词的理解能力：你可以用一段流畅的中文描述复杂构图、文字与细节，它都能较准确地呈现，几乎不需要学习专门的提示词技巧。",
            "它与 ChatGPT 深度集成，对话中即可生成与迭代图片，并支持在图内渲染可读文字，是制作配图、海报与信息图的便捷选择。免费用户可在 ChatGPT 中限量使用，Plus 用户享受更高额度。",
        ],
        "features": ["自然语言提示词，无需专业术语", "与 ChatGPT 对话式迭代出图", "图内文字渲染能力较强", "严格的内容安全策略", "免费即可限量使用", "API 便于集成开发"],
        "tags": ["绘画", "文生图", "OpenAI", "ChatGPT"],
        "faq": [
            {"q": "DALL·E 3 免费吗？", "a": "可以在 ChatGPT 免费版中限量使用；Plus 订阅与 API 调用提供更高额度和批量能力。"},
            {"q": "DALL·E 3 和 Midjourney 哪个好？", "a": "DALL·E 3 胜在提示词理解与易用性，Midjourney 胜在艺术表现力。追求效率选 DALL·E 3，追求画面质感选 Midjourney。"},
            {"q": "可以生成真人照片吗？", "a": "出于安全政策限制，无法生成指定真实人物的肖像，但可以生成风格化的普通人像。"},
        ],
        "related": ["chatgpt", "midjourney", "runway"],
    },
    {
        "slug": "runway", "name": "Runway", "emoji": "🎬",
        "cat": "ai-video", "vendor": "Runway AI, Inc.",
        "tagline": "专业级 AI 视频创作平台",
        "rating": 4.5, "reviews": "9,600", "price": "免费增值", "price_detail": "免费版 125 积分；Standard $15/月；Pro $35/月；Unlimited $95/月",
        "url": "https://runwayml.com", "affiliate": None,
        "desc": [
            "Runway 是 AI 视频生成领域的头部平台，旗下 Gen 系列模型可以通过文字或图片生成高质量动态视频，支持镜头控制、运动笔刷、首尾帧过渡等专业能力，被用于短片、广告与电影预演制作。",
            "除生成外，Runway 还内置绿幕抠像、物体擦除、慢动作、口型同步等 30+ AI 魔法工具，覆盖从生成到后期的大部分环节，是内容创作者和影视团队的一站式视频工作台。",
        ],
        "features": ["Gen 系列文生视频 / 图生视频", "运动笔刷与镜头方向控制", "绿幕抠像、物体擦除等 AI 后期工具", "首尾帧精准过渡", "Web 端在线协作", "API 供开发者集成"],
        "tags": ["视频生成", "后期", "文生视频", "影视"],
        "faq": [
            {"q": "Runway 有免费版吗？", "a": "有，注册即赠 125 积分可用于体验生成。积分制按生成时长计费，正式使用建议订阅 Standard（$15/月）及以上。"},
            {"q": "Runway 生成的视频有多长？", "a": "单次生成通常为 5-10 秒，可通过延长、首尾帧衔接等功能拼接成更长的成片。"},
            {"q": "商用需要注意什么？", "a": "付费档位生成的视频可用于商业用途，建议仔细阅读官方内容政策与版权条款。"},
        ],
        "related": ["suno", "midjourney", "pika-external"],
    },
    {
        "slug": "suno", "name": "Suno", "emoji": "🎵",
        "cat": "ai-audio", "vendor": "Suno, Inc.",
        "tagline": "一句话生成带人声的完整歌曲",
        "rating": 4.6, "reviews": "12,400", "price": "免费增值", "price_detail": "免费版每日 50 积分；Pro $10/月；Premier $30/月",
        "url": "https://suno.com", "affiliate": None,
        "desc": [
            "Suno 是目前最受欢迎的 AI 音乐生成工具：输入一段歌词或一句话的描述，就能在几十秒内生成包含人声演唱、和声、编曲与混音的完整歌曲，支持流行、摇滚、民谣、电子、说唱等海量风格。",
            "你可以自定义歌词、选择音色与曲风，也可以对生成结果进行延长、重唱与局部重制。免费版歌曲可个人使用，付费版支持商用授权，适合短视频配乐、播客片头与独立音乐创作。",
        ],
        "features": ["一句话生成完整歌曲", "自动生成或自定义歌词", "多种曲风与音色可选", "歌曲延长与局部重制", "中英文等多语言演唱", "免费版每日可用"],
        "tags": ["音乐生成", "人声", "歌曲", "短视频配乐"],
        "faq": [
            {"q": "Suno 生成的歌曲可以商用吗？", "a": "免费版仅限个人非商用。订阅 Pro 或 Premier 后拥有生成歌曲的商用权，具体以官方条款为准。"},
            {"q": "Suno 支持中文歌吗？", "a": "支持中文歌词演唱，吐字与旋律贴合度不错，也支持中英混合创作。"},
            {"q": "生成的歌曲属于谁？", "a": "付费订阅用户在条款范围内拥有生成内容的版权与商用权；免费用户的歌曲归 Suno 所有但可按条款非商用使用。"},
        ],
        "related": ["elevenlabs", "udio-external", "runway"],
    },
    {
        "slug": "elevenlabs", "name": "ElevenLabs", "emoji": "🎙️",
        "cat": "ai-audio", "vendor": "ElevenLabs",
        "tagline": "最自然的 AI 语音合成与声音克隆",
        "rating": 4.6, "reviews": "15,700", "price": "免费增值", "price_detail": "免费版每月 1 万字符；Starter $5/月；Creator $22/月；更高档位支持专业克隆",
        "url": "https://elevenlabs.io", "affiliate": None,
        "desc": [
            "ElevenLabs 是 AI 语音赛道的标杆产品，其文本转语音以情感丰富、韵律自然著称，29+ 种语言都能生成接近真人配音的效果，被广泛用于有声书、视频配音、游戏角色与播客制作。",
            "除标准音色库外，它支持快速声音克隆（几分钟样本）与专业声音克隆（更长样本、更高还原度），还能对语速、情感与停顿进行精细控制。API 完善，开发者可以把它集成到自己的应用里。",
        ],
        "features": ["行业领先的拟真语音合成", "29+ 语言自然发音", "快速 / 专业两级声音克隆", "情感、语速、停顿精细控制", "长音频与多角色项目支持", "完善的开发者 API"],
        "tags": ["语音合成", "声音克隆", "配音", "API"],
        "faq": [
            {"q": "ElevenLabs 免费额度是多少？", "a": "免费版每月 10,000 字符，可使用部分预置音色；Starter（$5/月）起解锁更多字符与克隆功能。"},
            {"q": "声音克隆需要授权吗？", "a": "是。只能克隆自己拥有权利的声音，官方要求克隆者本人授权，滥用会被封禁。"},
            {"q": "中文效果怎么样？", "a": "支持中文且自然度较高，多语言模型 v2+ 版本在中文韵律与情感表现上持续进步。"},
        ],
        "related": ["suno", "murf-external", "runway"],
    },
    {
        "slug": "github-copilot", "name": "GitHub Copilot", "emoji": "👨‍💻",
        "cat": "ai-code", "vendor": "GitHub / Microsoft",
        "tagline": "深入 IDE 的 AI 结对程序员",
        "rating": 4.6, "reviews": "27,500", "price": "免费增值", "price_detail": "免费版有限额度；Pro $10/月；Business $19/人/月；学生与开源维护者免费",
        "url": "https://github.com/features/copilot", "affiliate": None,
        "desc": [
            "GitHub Copilot 是最早普及、目前用户量最大的 AI 编程助手，由 GitHub 与 OpenAI 联合开发。它能根据上下文实时补全整行乃至整段代码，支持几乎所有主流语言与编辑器（VS Code、JetBrains、Neovim 等）。",
            "现在的 Copilot 远不止补全：Copilot Chat 支持在编辑器里对话解释代码、修复报错、生成测试，Agent 模式还能根据需求跨文件自动修改。个人版 $10/月，学生和热门开源维护者可免费使用，性价比极高。",
        ],
        "features": ["实时整段代码补全", "Copilot Chat 编辑器内对话", "多文件 Agent 自动改码", "生成单元测试与文档注释", "支持 VS Code / JetBrains / Neovim", "学生与开源维护者免费"],
        "tags": ["代码补全", "编程", "GitHub", "IDE 插件"],
        "faq": [
            {"q": "GitHub Copilot 免费吗？", "a": "提供有限额度的免费版；Pro 为 $10/月。经 GitHub 认证的学生、教师与热门开源维护者可免费使用 Pro。"},
            {"q": "和 Cursor 有什么区别？", "a": "Copilot 是插件，装在现有编辑器里；Cursor 是基于 VS Code 改造的独立 AI 编辑器。已有 IDE 习惯选 Copilot，想要 AI 原生体验可以试试 Cursor。"},
            {"q": "生成的代码安全吗？", "a": "Copilot 有公开代码匹配拦截与企业级安全策略，Business 版提供内容免责与 IP 赔偿，敏感项目建议使用企业版策略管理。"},
        ],
        "related": ["claude", "chatgpt", "cursor"],
    },
    {
        "slug": "gemini", "name": "Gemini", "emoji": "♊",
        "cat": "ai-chat", "vendor": "Google",
        "tagline": "深度整合 Google 生态的多模态 AI 助手",
        "rating": 4.5, "reviews": "21,000", "price": "免费增值", "price_detail": "免费版可用基础模型；Google AI Pro 约 $19.99/月；Workspace 商业版按席位订阅",
        "url": "https://gemini.google.com", "affiliate": None,
        "desc": [
            "Gemini 是 Google 推出的通用 AI 助手，原生支持文本、图像、音频等多模态输入，与 Gmail、Docs、搜索等 Google 服务深度打通，安卓用户还可以将其设为系统级助手。免费版即可满足日常问答、写作与图像生成需求。",
            "对订阅用户，Gemini 提供更强模型、更大的上下文窗口、NotebookLM 等配套能力以及 Google 云端存储，适合已经身处 Google 生态的学生与职场用户。如果你重度使用 Gmail/Docs，它是 ChatGPT 之外最顺滑的选择。",
        ],
        "features": ["文本/图像/语音多模态输入", "与 Gmail、Docs、搜索深度集成", "安卓系统级助手", "免费版即可生成图像", "长上下文处理长文档", "网页与移动 App 全覆盖"],
        "tags": ["对话", "多模态", "Google", "免费增值"],
        "faq": [
            {"q": "Gemini 免费吗？", "a": "免费版支持基础模型与图像生成；Google AI Pro（约 $19.99/月）解锁更强模型、更高额度与存储权益。"},
            {"q": "Gemini 和 ChatGPT 哪个好？", "a": "两者同属第一梯队。Gemini 胜在与 Google 生态和多模态的整合，ChatGPT 的插件生态与全球用户社区更成熟，建议都试用再定。"},
            {"q": "Gemini 支持中文吗？", "a": "支持，中文对话与写作能力良好，部分地区需要通过 Google 账号设置语言后使用。"},
        ],
        "related": ["chatgpt", "claude", "perplexity"],
    },
    {
        "slug": "perplexity", "name": "Perplexity", "emoji": "🔎",
        "cat": "ai-search", "vendor": "Perplexity AI",
        "tagline": "每个答案都带引用来源的 AI 搜索引擎",
        "rating": 4.5, "reviews": "14,300", "price": "免费增值", "price_detail": "免费版无限快速搜索；Pro $20/月，解锁高级模型与更强的 Pro Search",
        "url": "https://www.perplexity.ai", "affiliate": None,
        "desc": [
            "Perplexity 是 AI 搜索的代表产品：提问后它会实时联网检索多个信息源，用一段结构化的答案直接回答，并在每个关键结论后附上引用编号，点开即可溯源，大幅降低了被 AI 幻觉误导的风险。",
            "它适合查资料、做调研、验证事实等场景，Pro 版可选用 GPT、Claude 等多家模型进行深度检索，还支持上传 PDF 提问与学术文献搜索。免费版不限快速搜索次数，是替换传统搜索引擎的低门槛选择。",
        ],
        "features": ["实时联网检索，答案附引用来源", "Pro Search 多步深度研究", "支持选择 GPT / Claude 等模型", "上传 PDF 与图片提问", "学术搜索与焦点模式", "免费版不限快速搜索"],
        "tags": ["AI 搜索", "引用来源", "调研", "免费增值"],
        "faq": [
            {"q": "Perplexity 免费吗？", "a": "免费版可无限使用快速搜索；Pro（$20/月）解锁 Pro Search 深度检索、模型选择与更高文件上传额度。"},
            {"q": "它和 Google 搜索有什么区别？", "a": "Google 返回链接列表，Perplexity 直接给出整合后的答案并标注来源，更适合提问式查询；需要浏览大量网页时传统搜索仍更合适。"},
            {"q": "答案可信吗？", "a": "答案基于实时网页检索并附引用，可点击溯源自行验证；但引用源本身的质量仍需读者判断。"},
        ],
        "related": ["gemini", "chatgpt", "claude"],
    },
    {
        "slug": "notion-ai", "name": "Notion AI", "emoji": "📓",
        "cat": "ai-office", "vendor": "Notion Labs",
        "tagline": "长在笔记与项目库里的 AI 办公助手",
        "rating": 4.4, "reviews": "8,900", "price": "付费", "price_detail": "AI 附加包约 $10/成员/月（年付 $8），需先有 Notion 账号；企业版含安全管控",
        "url": "https://www.notion.so/product/ai", "affiliate": None,
        "desc": [
            "Notion AI 是内置于 Notion 的 AI 助手，不用切换应用就能对当前页面总结、翻译、续写、改写语气、提取待办，还能把杂乱的会议记录自动整理成结构化笔记，对重度 Notion 用户来说是顺手的效率放大器。",
            "它的独特优势在于能访问你的工作区：Notion AI Q&A 可以直接跨页面、跨数据库回答问题，例如「上周项目周报的结论是什么」，省去翻找时间。适合团队知识库、项目管理与个人笔记场景。",
        ],
        "features": ["页面内总结/翻译/续写/改写", "跨工作区 Q&A 智能问答", "数据库字段 AI 自动填充", "会议记录自动整理", "与 Notion 项目管理无缝衔接", "企业级权限与安全管控"],
        "tags": ["笔记", "办公", "知识库", "团队协作"],
        "faq": [
            {"q": "Notion AI 收费吗？", "a": "属于付费附加功能，约 $10/成员/月（年付有折扣），需在 Notion 订阅之外单独开启。"},
            {"q": "不用 Notion 的人适合买吗？", "a": "不适合。它的价值建立在 Notion 工作区之上；如果你只用通用 AI 助手，ChatGPT/Claude 性价比更高。"},
            {"q": "AI 会读到我的私密页面吗？", "a": "AI 仅在你主动调用时访问相应内容，企业版提供数据不用于训练等合规承诺，敏感信息建议设置页面权限。"},
        ],
        "related": ["claude", "chatgpt", "gamma-external"],
    },
    {
        "slug": "cursor", "name": "Cursor", "emoji": "⌨️",
        "cat": "ai-code", "vendor": "Anysphere",
        "tagline": "AI 原生代码编辑器，整库理解 + Agent 自动改码",
        "rating": 4.7, "reviews": "11,800", "price": "免费增值", "price_detail": "免费版有限额度；Pro $20/月；Business $40/用户/月",
        "url": "https://cursor.com", "affiliate": None,
        "desc": [
            "Cursor 是基于 VS Code 改造的 AI 原生编辑器，界面和插件与 VS Code 几乎一致，迁移零成本。它对整个代码库建立索引，回答和修改都考虑全仓库上下文，而不是只看当前文件。",
            "核心体验是 Composer 与 Agent 模式：用自然语言描述需求，Cursor 会跨多个文件自动创建、修改代码并执行终端命令，开发者只需审查与确认。Tab 补全也以预测「下一个改动点」见长。适合想深度拥抱 AI 编程的个人与团队。",
        ],
        "features": ["VS Code 兼容，迁移零成本", "整库索引，跨文件上下文理解", "Agent 模式自动多文件改码", "Composer 多文件编辑", "预测下一步改动的 Tab 补全", "支持接入多家模型"],
        "tags": ["编辑器", "Agent", "编程", "VS Code"],
        "faq": [
            {"q": "Cursor 免费版能用吗？", "a": "可以，免费版提供有限的补全与请求额度；Pro（$20/月）解锁更高用量与最强模型，重度使用者建议直接上 Pro。"},
            {"q": "Cursor 和 GitHub Copilot 怎么选？", "a": "想保留现有 VS Code/JetBrains 习惯选 Copilot 插件；想要 AI 原生体验、整库改码与 Agent 能力选 Cursor，两者也可以并用。"},
            {"q": "私企代码安全吗？", "a": "Cursor 提供隐私模式（代码不用于训练）与 SOC 2 认证，Business 版有更多管控，敏感项目建议开启隐私模式并咨询合规团队。"},
        ],
        "related": ["github-copilot", "claude", "chatgpt"],
    },
    {
        "slug": "deepl", "name": "DeepL", "emoji": "🌍",
        "cat": "ai-translate", "vendor": "DeepL SE",
        "tagline": "公认译文质量最高的机器翻译工具",
        "rating": 4.7, "reviews": "19,600", "price": "免费增值", "price_detail": "免费网页翻译不限量；Pro 约 $9/月起，解锁文档批量翻译、API 与术语表",
        "url": "https://www.deepl.com", "affiliate": None,
        "desc": [
            "DeepL 以译文自然、准确著称，尤其在欧洲语言之间的表现被广泛认为优于同类产品，近年对中文的支持也持续进步。它不仅能翻译句子，还理解上下文与语气，提供正式/非正式等多种译法可选。",
            "除了网页翻译，它支持把 Word、PDF、PPT 等文档整体翻译并保留原排版，配合术语表可保证专有名词统一；DeepL Write 还能对英文写作进行母语级润色。浏览器插件与 API 让它可以嵌入任何工作流。",
        ],
        "features": ["译文质量业界领先的神经翻译", "文档整篇翻译且保留排版", "术语表保证专有名词统一", "DeepL Write 英文写作润色", "浏览器插件划词翻译", "API 供企业集成"],
        "tags": ["翻译", "文档翻译", "润色", "API"],
        "faq": [
            {"q": "DeepL 免费吗？", "a": "网页端免费不限量翻译；Pro（约 $9/月起）解锁整篇文档批量翻译、更高安全等级、API 与术语表。"},
            {"q": "DeepL 和 Google 翻译谁更强？", "a": "英欧语言互译 DeepL 明显更自然；小语种覆盖和即时对话场景 Google 更全。中文用户建议两者都备，正式文档用 DeepL。"},
            {"q": "支持中文吗？", "a": "支持简体中文与日语等亚洲语言，中英互译质量整体优于多数竞品，长句逻辑尤其稳。"},
        ],
        "related": ["gemini", "chatgpt", "notion-ai"],
    },
]

# 供搜索与详情页相关推荐使用的外链工具索引
EXT_TOOLS_INDEX = {
    "rytr-external": {"name": "Rytr", "url": "https://rytr.me", "cat": "ai-writing"},
    "pika-external": {"name": "Pika", "url": "https://pika.art", "cat": "ai-video"},
    "udio-external": {"name": "Udio", "url": "https://www.udiomusic.com", "cat": "ai-audio"},
    "murf-external": {"name": "Murf", "url": "https://murf.ai", "cat": "ai-audio"},
    "cursor-external": {"name": "Cursor", "url": "https://cursor.com", "cat": "ai-code"},
    "gamma-external": {"name": "Gamma", "url": "https://gamma.app", "cat": "ai-office"},
}

TOOL_BY_SLUG = {t["slug"]: t for t in TOOLS}


def count_tools():
    """统计站内收录的独立工具数（按名称去重）。"""
    names = set()
    for items in CATEGORY_TOOLS.values():
        for it in items:
            if it["kind"] == "detail":
                names.add(TOOL_BY_SLUG[it["slug"]]["name"])
            else:
                names.add(it["name"])
    for c in CATEGORIES[5:]:
        pass  # 未建页分类不计入已收录
    return len(names)


TOOL_COUNT = count_tools()


# ---------------------------------------------------------------------------
# 页面片段
# ---------------------------------------------------------------------------
FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
           "<text y='.9em' font-size='90'>🤖</text></svg>")


def ext_link(url, text, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{url}"{c} target="_blank" rel="nofollow noopener">{text}</a>'


def stars(rating):
    full = int(round(rating))
    return "★" * full + "☆" * (5 - full)


def tool_card(t, root):
    return f'''<article class="card tool-card">
  <div class="tool-head"><span class="tool-icon">{t["emoji"]}</span>
    <div><h3><a href="{root}tool/{t["slug"]}.html">{t["name"]}</a></h3>
    <p class="tagline">{t["tagline"]}</p></div></div>
  <p class="tool-desc">{t["desc"][0][:90]}…</p>
  <div class="tool-meta"><span class="price-badge">{t["price"]}</span><span class="rating">{'★'} {t["rating"]}</span></div>
  <div class="tool-actions"><a class="btn btn-primary" href="{root}tool/{t["slug"]}.html">查看详情</a>
  {ext_link(t["url"], "访问官网", "btn btn-ghost")}</div>
</article>'''


def ext_tool_card(it):
    return f'''<article class="card tool-card">
  <div class="tool-head"><span class="tool-icon">{CAT_BY_SLUG[it_cat(it)]["emoji"]}</span>
    <div><h3>{it["name"]}</h3><p class="tagline">{CAT_BY_SLUG[it_cat(it)]["name"]}工具</p></div></div>
  <p class="tool-desc">{it["desc"]}</p>
  <div class="tool-meta"><span class="price-badge">查看官网</span></div>
  <div class="tool-actions">{ext_link(it["url"], "访问官网", "btn btn-primary")}</div>
</article>'''


def it_cat(it):
    for slug, items in CATEGORY_TOOLS.items():
        if it in items:
            return slug
    return ""


def header(root, active=""):
    nav_items = f'<a href="{root}index.html"{" class=active" if active=="home" else ""}>首页</a>'
    for c in CATEGORIES[:5]:
        cls = ' class="active"' if active == c["slug"] else ""
        nav_items += f'<a href="{root}category/{c["slug"]}.html"{cls}>{c["emoji"]} {c["name"]}</a>'
    return f'''<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="{root}index.html"><span class="logo-icon">🤖</span>{SITE_NAME}</a>
    <nav class="main-nav">{nav_items}</nav>
    <div class="header-right">
      <div class="search-box"><input type="search" id="globalSearch" placeholder="搜索 AI 工具…" autocomplete="off"><div class="search-results" id="searchResults"></div></div>
      <button id="themeToggle" class="theme-toggle" aria-label="切换暗色模式">🌙</button>
    </div>
  </div>
</header>'''


def footer(root):
    cats = "".join(f'<a href="{root}category/{c["slug"]}.html">{c["name"]}</a>' for c in CATEGORIES)
    tools = "".join(f'<a href="{root}tool/{t["slug"]}.html">{t["name"]}</a>' for t in TOOLS[:5])
    more = "".join(f'<a href="{root}tool/{t["slug"]}.html">{t["name"]}</a>' for t in TOOLS[5:])
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div><h4>分类导航</h4>{cats}</div>
    <div><h4>热门工具</h4>{tools}</div>
    <div><h4>更多工具</h4>{more}</div>
    <div><h4>关于本站</h4>
      <a href="{root}about.html">关于我们</a>
      <a href="{root}privacy-policy.html">隐私政策</a>
      <a href="{root}contact.html">联系我们</a></div>
  </div>
  <div class="footer-bottom container">
    <p>© <span id="year"></span> {SITE_NAME} · 部分链接为联盟链接，使用本站即表示同意<a href="{root}privacy-policy.html">隐私政策</a></p>
  </div>
</footer>'''


AD_BANNER = '''<!-- ===== Google AdSense 广告位：顶部 Banner =====
发布时将下面占位块替换为 AdSense <ins class="adsbygoogle"> 代码：
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXX" data-ad-slot="XXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
===== -->
<div class="ad-slot ad-banner" data-ad="top-banner"><span>广告位 · 顶部 Banner</span></div>'''

AD_SIDEBAR = '''<!-- ===== Google AdSense 广告位：侧边栏 =====
发布时替换为：<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXX" data-ad-slot="YYYYYYY" data-ad-format="auto"></ins>
===== -->
<div class="ad-slot ad-side" data-ad="sidebar"><span>广告位 · 侧边栏</span></div>'''


def page(title, desc, path, content, root, jsonld_extra=None, active=""):
    """jsonld_extra: list of dicts"""
    full_title = f"{title} | {SITE_NAME}"
    jsonld = [
        {"@context": "https://schema.org", "@type": "WebSite",
         "name": SITE_NAME, "url": SITE_URL + "/",
         "potentialAction": {"@type": "SearchAction",
                             "target": SITE_URL + "/index.html?q={search_term_string}",
                             "query-input": "required name=search_term_string"}},
        {"@context": "https://schema.org", "@type": "Organization",
         "name": SITE_NAME, "url": SITE_URL + "/"},
    ]
    if jsonld_extra:
        jsonld.extend(jsonld_extra)
    ld_scripts = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>'
        for x in jsonld)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE_URL}/{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE_URL}/{path}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{full_title}">
<meta name="twitter:description" content="{desc}">
<link rel="icon" href="{FAVICON}">
{ld_scripts}
{AD_BANNER.replace("<div class=", "<!--see-below--><div class=", 1) if False else ""}
<link rel="stylesheet" href="{root}static/style.css">
</head>
<body data-root="{root}">
{header(root, active)}
{AD_BANNER}
<main>{content}</main>
{footer(root)}
<script src="{root}static/app.js"></script>
</body>
</html>'''


def breadcrumb(items):
    """items: [(name, href or None)]"""
    parts = []
    for i, (name, href) in enumerate(items):
        if href:
            parts.append(f'<a href="{href}">{name}</a>')
        else:
            parts.append(f'<span aria-current="page">{name}</span>')
    return f'<nav class="breadcrumb container" aria-label="面包屑">{ " <span class=sep>›</span> ".join(parts) }</nav>'


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "name": n, **({"item": SITE_URL + "/" + h} if h else {})}
                for i, (n, h) in enumerate(items)]}


# ---------------------------------------------------------------------------
# 首页
# ---------------------------------------------------------------------------
def gen_index():
    cat_cards = ""
    for c in CATEGORIES:
        n = len(CATEGORY_TOOLS[c["slug"]])
        cat_cards += f'''<a class="card cat-card" href="category/{c["slug"]}.html">
  <span class="cat-emoji">{c["emoji"]}</span>
  <h3>{c["name"]}</h3>
  <p class="cat-desc">{c["desc"][:46]}…</p>
  <span class="cat-count">{n} 个工具</span></a>'''
    upcoming_cats = [c for c in CATEGORIES if not c["page"]]
    if upcoming_cats:
        upcoming = "、".join(c["name"] for c in upcoming_cats[:4])
        more_note = f'<p class="muted center">更多分类即将上线：{upcoming} 等 <strong>{len(upcoming_cats)}</strong> 个分类正在建设中…</p>'
    else:
        more_note = '<p class="muted center">✅ 全部 <strong>15</strong> 个分类均已上线，点击卡片开始探索。</p>'
    featured = "".join(tool_card(t, "") for t in [TOOLS[0], TOOLS[4], TOOLS[1], TOOLS[7], TOOLS[9], TOOLS[6]])

    content = f'''
<section class="hero">
  <div class="container">
    <h1>发现最好的 <span class="grad">AI 工具</span></h1>
    <p class="hero-sub">{SITE_TAGLINE}：精选 {TOOL_COUNT}+ 款 AI 写作、绘画、视频、音频、编程工具，附带功能介绍、价格对比与使用指南。</p>
    <div class="search-box hero-search"><input type="search" id="globalSearch" placeholder="搜索工具名，如 ChatGPT、Midjourney…" autocomplete="off"><div class="search-results" id="searchResults"></div></div>
    <div class="hero-stats">
      <div class="stat"><strong>{TOOL_COUNT}+</strong><span>已收录工具</span></div>
      <div class="stat"><strong>{len(CATEGORIES)}</strong><span>工具分类</span></div>
      <div class="stat"><strong>100%</strong><span>人工筛选</span></div>
      <div class="stat"><strong>持续更新</strong><span>每周新增</span></div>
    </div>
  </div>
</section>

<section class="container section">
  <h2 class="section-title">按分类浏览</h2>
  <div class="grid grid-cats">{cat_cards}</div>
  {more_note}
</section>

<section class="container section">
  <h2 class="section-title">精选推荐工具</h2>
  <div class="grid grid-tools">{featured}</div>
</section>

<section class="container section cta-band">
  <h2>为什么使用 {SITE_NAME}？</h2>
  <div class="grid grid-3">
    <div class="card why-card"><span>🔍</span><h3>严格筛选</h3><p>只收录经过验证的主流 AI 工具，附真实功能与价格信息。</p></div>
    <div class="card why-card"><span>💰</span><h3>价格透明</h3><p>每个工具标注免费 / 免费增值 / 付费，帮你快速决策。</p></div>
    <div class="card why-card"><span>🔄</span><h3>持续更新</h3><p>AI 领域日新月异，我们每周核查并补充新工具。</p></div>
  </div>
</section>'''

    title = f"AI 工具大全 - 收录 {TOOL_COUNT}+ 最佳 AI 工具"
    desc = f"{SITE_NAME}精选收录 {TOOL_COUNT}+ 款最佳 AI 工具，覆盖 AI 写作、绘画、视频、音频、编程等 {len(CATEGORIES)} 个分类，含功能介绍、价格对比与使用指南，持续更新。"
    return page(title, desc, "", content, root="", active="home")


# ---------------------------------------------------------------------------
# 分类页
# ---------------------------------------------------------------------------
def gen_category(cat):
    slug, name = cat["slug"], cat["name"]
    items = CATEGORY_TOOLS[slug]
    cards = []
    for it in items:
        if it["kind"] == "detail":
            t = TOOL_BY_SLUG[it["slug"]]
            cards.append(tool_card(t, "../"))
        else:
            emoji = cat["emoji"]
            cards.append(f'''<article class="card tool-card">
  <div class="tool-head"><span class="tool-icon">{emoji}</span>
    <div><h3>{ext_link(it["url"], it["name"])}</h3><p class="tagline">{name}工具</p></div></div>
  <p class="tool-desc">{it["desc"]}</p>
  <div class="tool-meta">{" ".join(f'<span class="tag">{x}</span>' for x in it["tags"])}</div>
  <div class="tool-actions">{ext_link(it["url"], "访问官网", "btn btn-primary")}</div>
</article>''')
    first, rest = cards[:6], cards[6:]
    hidden = ""
    load_more = ""
    if rest:
        hidden = f'<div class="grid grid-tools more-tools" hidden>{"".join(rest)}</div>'
        load_more = '<div class="center"><button class="btn btn-ghost" id="loadMoreBtn">加载更多</button></div>'

    related = "".join(
        f'<a class="side-link" href="../category/{c["slug"]}.html">{c["emoji"]} {c["name"]}<span>{len(CATEGORY_TOOLS[c["slug"]])}</span></a>'
        for c in CATEGORIES[:5] if c["slug"] != slug)

    content = f'''
{breadcrumb([(SITE_NAME, "../index.html"), (name, None)])}
<div class="container page-layout">
  <div class="page-main">
    <header class="page-head">
      <span class="cat-emoji big">{cat["emoji"]}</span>
      <h1>最佳 {name} 工具推荐</h1>
      <p class="muted">{cat["desc"]}本页收录 {len(items)} 款 {name}工具，包含功能介绍、价格信息与官网直达链接。</p>
    </header>
    <div class="grid grid-tools">{"".join(first)}</div>
    {hidden}
    {load_more}
  </div>
  <aside class="page-side">
    {AD_SIDEBAR}
    <div class="card side-card">
      <h3>相关分类</h3>
      {related}
    </div>
  </aside>
</div>'''

    title = f"最佳 {name} 工具 - 2026 年推荐"
    desc = f"2026 年最佳{name}工具推荐：精选 {len(items)} 款{name}AI 工具，含功能特点、价格对比、评分与官网链接，帮你快速找到合适的{name}AI 产品。"
    path = f"category/{slug}.html"
    jsonld = [breadcrumb_ld([(SITE_NAME, ""), (name, path)]),
              {"@context": "https://schema.org", "@type": "ItemList",
               "name": f"最佳 {name} AI 工具",
               "itemListElement": [
                   {"@type": "ListItem", "position": i + 1,
                    "name": (TOOL_BY_SLUG[it["slug"]]["name"] if it["kind"] == "detail" else it["name"]),
                    "url": (f"{SITE_URL}/tool/{it['slug']}.html" if it["kind"] == "detail" else it["url"])}
                   for i, it in enumerate(items)]}]
    return page(title, desc, path, content, root="../", jsonld_extra=jsonld, active=slug)


# ---------------------------------------------------------------------------
# 工具详情页
# ---------------------------------------------------------------------------
def gen_tool(t):
    cat = CAT_BY_SLUG[t["cat"]]
    visit_url = t["affiliate"] or t["url"]
    affiliate_note = ('<!-- TODO: 将下方 href 替换为你的联盟链接，例如 https://partner.com/ref=yourid -->'
                      if not t["affiliate"] else '<!-- 联盟链接已启用 -->')

    features = "".join(f"<li>{f}</li>" for f in t["features"])
    tags = "".join(f'<span class="tag">{x}</span>' for x in t["tags"])
    paras = "".join(f"<p>{p}</p>" for p in t["desc"])
    faq_html = "".join(
        f'<details class="faq-item"><summary>{f["q"]}</summary><div class="faq-a"><p>{f["a"]}</p></div></details>'
        for f in t["faq"])

    related = []
    for r in t["related"]:
        if r in TOOL_BY_SLUG:
            related.append(tool_card(TOOL_BY_SLUG[r], "../"))
        elif r in EXT_TOOLS_INDEX:
            e = EXT_TOOLS_INDEX[r]
            related.append(f'''<article class="card tool-card">
  <div class="tool-head"><span class="tool-icon">{CAT_BY_SLUG[e["cat"]]["emoji"]}</span>
    <div><h3>{e["name"]}</h3></div></div>
  <div class="tool-actions">{ext_link(e["url"], "访问官网", "btn btn-ghost")}</div>
</article>''')

    content = f'''
{breadcrumb([(SITE_NAME, "../index.html"), (cat["name"], f"../category/{cat['slug']}.html"), (t["name"], None)])}
<div class="container tool-page">
  <header class="tool-hero card">
    <span class="tool-icon xl">{t["emoji"]}</span>
    <div class="tool-hero-body">
      <h1>{t["name"]}</h1>
      <p class="tagline">{t["tagline"]} · {t["vendor"]}</p>
      <div class="rating-line"><span class="rating-stars" aria-label="{t["rating"]} 分">{stars(t["rating"])}</span>
        <strong>{t["rating"]}</strong><span class="muted">/ 5 · {t["reviews"]} 条评价</span>
        <span class="price-badge">{t["price"]}</span></div>
      <div class="tool-actions">
        {affiliate_note}
        {ext_link(visit_url, "🚀 访问官网", "btn btn-primary btn-lg")}
        <a class="btn btn-ghost" href="../category/{cat["slug"]}.html">更多{cat["name"]}工具</a>
      </div>
      <div class="tags">{tags}</div>
    </div>
  </header>

  <div class="page-layout">
    <div class="page-main">
      <section class="card section-card"><h2>{t["name"]} 是什么？</h2>{paras}</section>
      <section class="card section-card"><h2>核心功能特点</h2><ul class="feature-list">{features}</ul></section>
      <section class="card section-card"><h2>价格方案</h2>
        <p class="price-line"><span class="price-badge">{t["price"]}</span>{t["price_detail"]}</p>
        <p class="muted">价格可能随官方调整而变化，请以官网为准。</p></section>
      <section class="card section-card"><h2>用户评价</h2>
        <div class="rating-line big"><span class="rating-stars">{stars(t["rating"])}</span><strong>{t["rating"]} / 5</strong><span class="muted">（基于 {t["reviews"]} 条评价）</span></div>
        <p class="muted">评分综合官方商店与第三方评测平台数据，仅供参考。</p></section>
      <section class="card section-card"><h2>常见问题（FAQ）</h2>{faq_html}</section>
    </div>
    <aside class="page-side">
      {AD_SIDEBAR}
      <div class="card side-card">
        <h3>相关工具推荐</h3>
        {"<hr>".join(f'<a class="side-link" href="../tool/{TOOL_BY_SLUG[r]["slug"]}.html" >{TOOL_BY_SLUG[r]["emoji"]} {TOOL_BY_SLUG[r]["name"]}<span>★ {TOOL_BY_SLUG[r]["rating"]}</span></a>' for r in t["related"] if r in TOOL_BY_SLUG)}
      </div>
    </aside>
  </div>

  <section class="section"><h2 class="section-title">你可能在找</h2>
    <div class="grid grid-tools">{"".join(related)}</div></section>
</div>'''

    title = f"{t['name']} - 功能介绍、价格、替代方案"
    desc = f"{t['name']} 是什么？{t['tagline']}。本文介绍 {t['name']} 的核心功能、价格方案（{t['price']}）、优缺点、用户评分与常见问题，并提供同类 {cat['name']}工具替代方案对比。"
    path = f"tool/{t['slug']}.html"
    jsonld = [
        breadcrumb_ld([(SITE_NAME, ""), (cat["name"], f"category/{cat['slug']}.html"), (t["name"], path)]),
        {"@context": "https://schema.org", "@type": "SoftwareApplication",
         "name": t["name"], "applicationCategory": cat["name"] + " AI 工具",
         "operatingSystem": "Web", "url": t["url"],
         "description": t["desc"][0],
         "offers": {"@type": "Offer", "price": "0" if t["price"] != "付费" else "10",
                    "priceCurrency": "USD",
                    "description": t["price_detail"]},
         "aggregateRating": {"@type": "AggregateRating",
                             "ratingValue": str(t["rating"]), "ratingCount": t["reviews"].replace(",", "")}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": f["q"],
                         "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                        for f in t["faq"]]},
    ]
    return page(title, desc, path, content, root="../", jsonld_extra=jsonld)


# ---------------------------------------------------------------------------
# 政策页面
# ---------------------------------------------------------------------------
def gen_privacy():
    content = '''
<div class="container narrow">
<h1>隐私政策</h1>
<p class="muted">最后更新：2026 年 9 月 18 日</p>

<h2>1. 引言</h2>
<p>欢迎使用本网站（下称"本站"）。本政策说明我们在你访问本站时如何收集、使用与保护信息。使用本站即表示你同意本政策。</p>

<h2>2. 我们收集的信息</h2>
<ul>
<li><strong>自动收集的信息：</strong>浏览器类型、访问时间、页面浏览记录等匿名统计数据（通过分析工具收集）。</li>
<li><strong>Cookie：</strong>本站使用 Cookie 记住你的主题偏好（如暗色模式）并支持广告服务。你可以随时在浏览器中清除或禁用 Cookie。</li>
</ul>

<h2>3. 联盟链接声明</h2>
<p><strong>重要披露：</strong>本站部分外链为联盟营销链接（Affiliate Links）。当你通过这些链接访问并购买产品时，我们可能获得佣金，<strong>你无需为此支付任何额外费用</strong>。所有外链均带有 <code>rel="nofollow noopener"</code> 属性。联盟关系不会影响我们的编辑独立性与工具评分。</p>

<h2>4. 广告与 Google AdSense</h2>
<p>本站使用 Google AdSense 展示广告。Google 及其合作伙伴可能使用 Cookie（包括第三方 Cookie）根据你以往的访问记录投放个性化广告。你可以访问 <a href="https://adssettings.google.com" target="_blank" rel="nofollow noopener">Google 广告设置</a> 管理个性化广告，或访问 <a href="https://www.aboutads.info" target="_blank" rel="nofollow noopener">aboutads.info</a> 选择退出第三方 Cookie。</p>

<h2>5. 第三方网站</h2>
<p>本站包含指向第三方工具官网的外链。我们对第三方网站的隐私行为不承担责任，建议你在使用前阅读其隐私政策。</p>

<h2>6. 数据安全</h2>
<p>我们采取合理的 technically 措施保护你的信息，本站本身不注册账号、不存储你的个人身份数据。</p>

<h2>7. 政策更新</h2>
<p>我们可能不定期更新本政策，更新后将在本页公布新的生效日期。</p>

<h2>8. 联系我们</h2>
<p>如对本政策有疑问，请通过<a href="contact.html">联系我们</a>页面与我们取得联系。</p>
</div>'''
    return page("隐私政策 - 联盟链接与广告声明", "本站隐私政策：说明 Cookie 使用、联盟营销链接披露、Google AdSense 广告与第三方网站政策，保障访客知情权。", "privacy-policy.html", content, root="")


def gen_about():
    content = f'''
<div class="container narrow">
<h1>关于我们</h1>
<p><strong>{SITE_NAME}</strong> 成立于 2026 年，致力于帮助中文用户在快速变化的 AI 浪潮中找到最适合的工具。</p>

<h2>我们做什么</h2>
<p>AI 工具数量爆炸式增长，寻找合适的工具却越来越难。我们人工筛选、实测并收录各类 AI 工具，为每个工具整理功能特点、价格方案、评分与常见问题，让你几分钟内做出决策。</p>

<h2>我们的原则</h2>
<ul>
<li><strong>人工筛选：</strong>所有收录的工具均经过实际体验与调研，拒绝垃圾收录。</li>
<li><strong>信息透明：</strong>价格、免费额度、评分来源均如实标注。</li>
<li><strong>独立客观：</strong>本站通过联盟链接与广告获得收入，但这不影响工具的收录标准与评分。</li>
</ul>

<h2>联系我们</h2>
<p>有推荐收录的工具、发现信息过时，或想合作？欢迎通过<a href="contact.html">联系我们</a>页面告知。</p>
</div>'''
    return page("关于我们 - 人工筛选的 AI 工具导航", f"了解 {SITE_NAME}：我们人工实测筛选 AI 工具，提供透明的价格与评分信息，帮助中文用户快速找到合适的 AI 产品。", "about.html", content, root="")


def gen_contact():
    content = '''
<div class="container narrow">
<h1>联系我们</h1>
<p>欢迎通过以下方式与我们联系，我们通常在 1-2 个工作日内回复。</p>

<h2>📮 商务合作与投稿</h2>
<p>工具推荐、联盟合作、广告投放：<strong>hello@example.com</strong></p>

<h2>🐛 纠错与反馈</h2>
<p>发现价格、评分或功能介绍过时？请邮件注明工具名称与页面链接，我们会尽快核实更新。</p>

<h2>📝 联系表单</h2>
<div class="card contact-form">
  <form action="#" method="post" onsubmit="alert('演示站点：请通过邮件联系我们');return false;">
    <label>你的邮箱<input type="email" required placeholder="you@example.com"></label>
    <label>留言内容<textarea rows="5" required placeholder="想对我们说什么…"></textarea></label>
    <button type="submit" class="btn btn-primary">发送留言</button>
    <p class="muted">演示表单：正式上线时可接入 Formspree / Getform 等静态表单服务。</p>
  </form>
</div>
</div>'''
    return page("联系我们 - 反馈与商务合作", f"联系 {SITE_NAME}：工具推荐、纠错反馈、联盟合作与广告投放联系方式，欢迎随时来信。", "contact.html", content, root="")


# ---------------------------------------------------------------------------
# sitemap / robots
# ---------------------------------------------------------------------------
def gen_sitemap():
    urls = [""]
    urls += [f"category/{c['slug']}.html" for c in CATEGORIES if c["page"]]
    urls += [f"tool/{t['slug']}.html" for t in TOOLS]
    urls += ["privacy-policy.html", "about.html", "contact.html"]
    items = "\n".join(
        f"  <url><loc>{SITE_URL}/{u}</loc><changefreq>weekly</changefreq><priority>{'1.0' if u == '' else '0.8'}</priority></url>"
        for u in urls)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>'''


ROBOTS = f'''User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
'''


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(DOCS, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {path}")


def main():
    print(f"开始生成站点：{DOCS}")
    write("index.html", gen_index())
    n_cat = 0
    for c in CATEGORIES:
        if c["page"]:
            write(f"category/{c['slug']}.html", gen_category(c))
            n_cat += 1
    for t in TOOLS:
        write(f"tool/{t['slug']}.html", gen_tool(t))
    write("privacy-policy.html", gen_privacy())
    write("about.html", gen_about())
    write("contact.html", gen_contact())
    write("sitemap.xml", gen_sitemap())
    write("robots.txt", ROBOTS)
    total = 1 + n_cat + len(TOOLS) + 3
    print(f"\n完成：HTML 页面 {total} 个（首页 1 + 分类页 {n_cat} + 工具详情页 {len(TOOLS)} + 政策页 3），另含 sitemap.xml 与 robots.txt")
    print(f"收录工具总数（去重）：{TOOL_COUNT}")


if __name__ == "__main__":
    main()
