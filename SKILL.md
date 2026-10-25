---
title: "通神兵器库 v1.0"
summary: "通神系统全部有用Skill的封存索引 + API凭证 + 使用方法"
description: "通神兵器库 — 封存全部有用Skill的索引目录、API凭证、MCP配置、使用方法。一键迁移，一键查阅。触发词：兵器库、skill索引、skill列表、通神skill、armory、所有skill、技能总览。"
agent_created: true
version: "1.0.0"
created: "2026-06-21"
---

# 通神兵器库 v1.0

> 程天居中调度，五行各司其职。兵器库一键封存，迁移无忧。

---

## 一、API 凭证（永久固定）

| 服务 | Key | 状态 | 备注 |
|------|-----|------|------|
| Firecrawl | `fc-7f6c51167e4d4c4abe925b8d179ae30d` | ✅ 已写入 mcp.json | 长期有效 |
| GitHub PAT | `ghp_YOUR_TOKEN_PLACEHOLDER` | ✅ 已写入 mcp.json | **2027-06-15 到期** |
| 微信公众号 APP_ID | `wx3d0126d5a6020045` | ✅ 已写入 config.py | |
| 微信公众号 APP_SECRET | `a6bc3af9f36ad78082a75b0d8fcb263e` | ✅ 已写入 config.py | |
| 微信公众号 IP白名单 | `183.46.128.45` | ✅ 微信后台已配置 | |

**迁移指令**：将以上值写入目标环境的 `~/.workbuddy/mcp.json` 对应 `env` 字段 + `~/.workbuddy/skills/wechat-publisher/scripts/config.py`。

**GitHub PAT 续期提醒**：已设置 2027-06-01 自动提醒（automation ID: automation-1781971319528）。

---

## 二、MCP 服务器配置（10个）

| 服务器 | 用途 | 状态 |
|--------|------|------|
| filesystem | 本地文件系统访问 | ✅ |
| github | GitHub API 操作 | ✅ 已填入真实Token |
| fetch | HTTP 请求抓取 | ✅ |
| memory | 持久化记忆存储 | ✅ |
| sequential-thinking | 链式推理 | ✅ |
| puppeteer | 浏览器自动化(无头) | ✅ |
| context7 | 文档上下文检索 | ✅ |
| firecrawl | 增强网页抓取 | ✅ 已填入真实Key |
| playwright | 浏览器自动化(现代) | ✅ |
| sqlite | 交易数据库 | ✅ |

**平台 Connector（已连接）**：飞书、乐享知识库、腾讯文档、IMA知识库

---

## 三、Skill 全景索引（按领域分类）

### 3.1 通神核心（7个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `tongshen-v8.1` | 通神、调度、路由 | 全域调度核心，M0元认知+7域路由+链式执行 |
| `tongshen-anti-truncation` | 截断、反截断、truncation | 上下文压缩+分段协议+逃生机制 |
| `tongshen-team-dispatch` | 团队调度、dispatch | 多Agent团队调度 |
| `self-evolution` | 复盘、自进化、反思 | 弱点复盘+系统自进化 |
| `info-compressor` | 压缩、compressor | 三层信息压缩，降Token开销 |
| `task-chain` | 任务链、chain | 绕过输出长度限制，链式推进 |
| `dmp-skill-logger` | 日志、logger | 跨平台任务历史记录 |

### 3.2 交易/量化（7个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `trading-analysis` | 金价、黄金、XAUUSD、交易分析 | 金易明四维分析(技术/基本/情绪/地缘) |
| `volbreak-backtest` | 回测、backtest | VolBreak Pro 回测引擎，M3/M15/H1 |
| `volbreak-auto-trading` | 自动交易、volbreak、auto trade | 全自动量化引擎，XAUUSD胜率90.4% |
| `vb-pro-btceth-detection` | BTC检测、ETH检测、3分钟 | BTCUSD/ETHUSD 3分钟循环检测 |
| `xauusd-daily-strategy` | AegisXAU、黄金策略 | ICT_MA策略EA+Python守护进程 |
| `mt5-swing-trader-system` | MT5、EA、swing | 波动结构HH/HL/LH/LL全栈系统 |
| `wallstreet-trading-closed-loop` | 交易闭环、华尔街天团 | 多专家协同全自动交易闭环 |

### 3.3 内容/公众号（12个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `wechat-publisher` | 发公众号、公众号发布 | 微信公众号排版推送+8平台分发 |
| `diyi-daily` | 帝意日报、今日推送 | 热点→排行榜+6篇副文→推送公众号 |
| `diyi-intro-video` | 帝意视频、品牌介绍视频 | 9:16竖版品牌介绍短视频 |
| `diyi-video-producer` | 生成视频、排行榜视频 | 数据驱动视频自动化生产 |
| `weixin-article-writer` | 写公众号、财经文章 | 财新风格财经投资类文章 |
| `content-factory-pipeline` | 内容流水线、批量内容 | 多平台内容批量生产 |
| `explosive-cover-generator-gzh` | 公众号封面、爆款封面 | AI封面设计 |
| `daily-batch-publisher` | 批量发布、daily batch | 每日批量发布 |
| `wechat-article-search` | 搜索公众号文章 | 微信搜索获取文章列表 |
| `wechat-article-pro` | 公众号文章专业版 | 联网搜索+封面+撰写+发布全流程 |
| `wechat-viral-topic` | 爆款选题、viral topic | 热点爆款策划助手 |
| `khazix-writer` | 卡兹克、公众号长文 | 公众号长文写作 |

### 3.4 浏览器/自动化（4个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `opencli-agent` | opencli、社交媒体操作 | 70+平台命令行自动化 |
| `tencent-novnc-chromium-cdp` | 自动发抖音、自动发小红书 | noVNC+Chromium+CDP三合一 |
| `douyin-copy-extract` | 抖音文案、视频文案提取 | 短视频文案提取 |
| `smooth-browser` (skill_2053082732028436480) | 浏览器、browser | 首选浏览器自动化 |

### 3.5 视频/图像（5个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `hyperframes` | HyperFrames、视频 | HTML/CSS/JS编写视频，9大工作流 |
| `hyperframes-portable` | HyperFrames便携版 | 路径固化，直接lint→render |
| `hyperframes-video-suite` | 视频流水线 | 环境固化+完整SOP+模板 |
| `openclaw-v3` | 视频生成、文生视频 | 火山引擎SD1.5pro API |
| `libtv-skill` | libtv、图片生成 | AI生成和编辑图片/视频 |

### 3.6 研究/数据（5个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `deep-research` | 深度调研、benchmark | 深度研究+对比分析 |
| `hot` | 热搜、热榜、排行榜 | 中国实时热点数据采集 |
| `macro-monitor` (skill_2053082337409794048) | 宏观、macro | 每日宏观数据监控推送 |
| `perplexity` (skill_2053082581570363392) | perplexity、AI搜索 | AI驱动网页搜索 |
| `multi-search-engine` (skill_2053082413554933760) | 多搜索引擎 | 16搜索引擎集成 |

### 3.7 开发/部署（6个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `deploy-website` | 部署网站、deploy | 网站部署 |
| `ui-new` | UI界面、设计页面 | 专业UI生成与优化 |
| `web-deploy` (skill_2054901554596478976) | web部署 | 构建+预览+部署 |
| `html-deploy` (skill_2054901495867834368) | HTML部署 | 单页HTML发布到公网 |
| `vercel-deploy` (skill_2054902267853770752) | Vercel部署 | Vercel项目管理 |
| `github-pages-auto-deploy` (skill_2054901716814716928) | GitHub Pages | 自动部署到GitHub Pages |

### 3.8 GitHub 工具（5个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `github-cli` | gh、github cli | GitHub CLI完整参考 |
| `github-helper` | github helper | 本地仓库搜索/克隆/同步 |
| `github-kb` | github kb | 本地GitHub知识库管理 |
| `github-manager` | github管理 | GitHub仓库管理 |
| `github-token` | github token | PAT方式操作GitHub |

### 3.9 AI/Coze（3个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `coze` | 扣子、coze、bot开发 | Coze Bot开发助手 |
| `coze-image-2` | coze图片、seedream | Seedream 4.5图片生成 |
| `delonix-coze-cli` | coze cli、扣子CLI | Coze CLI项目创建/部署 |

### 3.10 小说/创作（4个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `fiction-crafter` | 小说、爽文、写作 | 自动生成提示词+创作爽文 |
| `novel-writer` (skill_2053082474668232704) | 章节正文、novel | 章节正文生成器 |
| `novel-writing` (skill_2053082488455954432) | 长篇网文、novel writing | AI长篇网文创作 |
| `g113593` | 番茄小说、tomato | 番茄小说平台分章创作 |

### 3.11 工具类（15个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `md-to-pdf-cjk` (skill_2053082374000742400) | MD转PDF | Markdown转专业PDF(CJK) |
| `markitdown-skill` (skill_2053083553754644480) | markitdown、文件转换 | PDF/Word/PPT/图片→Markdown |
| `summarize` (skill_2053082894098632704) | 总结、summarize | URL/文件摘要 |
| `canvas-design` (skill_2053081626394972160) | 设计、canvas | 生成PNG/PDF视觉艺术 |
| `humanizer` (skill_2053082097175687168) | 去AI味、humanize | 去除AI生成痕迹 |
| `openai-image-gen` (skill_2053082508268802048) | 生成图片、openai image | OpenAI Images API批量生成 |
| `nano-banana-pro` (skill_2053082421296758784) | nano banana、图片编辑 | Gemini图片生成/编辑 |
| `gifgrep` (skill_2053082027064852480) | GIF搜索、gifgrep | GIF搜索下载 |
| `skills-security-check` (skill_2053082711420960768) | 安全检查、skill审计 | 腾讯云鼎实验室安全审查 |
| `skill-creator` (skill_2053082698440450048) | 创建skill、skill-creator | Skill创建指南 |
| `paper-quick-reader` (skill_2057443697088589824) | 论文速读、paper | AI论文三档深度阅读 |
| `web-access` (skill_2053083109158420480) | 联网、web access | 所有联网操作统一入口 |
| `obsidian` (skill_2053082563940843521) | obsidian、笔记 | Obsidian vault操作 |
| `gmail` (skill_2053082044158386176) | gmail、邮件 | Gmail API集成 |
| `lark-unified` (skill_2053082253572640768) | 飞书、lark | 飞书CLI套件 |

### 3.12 其他（5个）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `computer-vision-expert` | CV、计算机视觉 | YOLO26/SAM3/VLM专家 |
| `yolo-vision-tools` | YOLO、检测 | Ultralytics YOLO计算机视觉 |
| `travel-cn` | 旅行、机票、酒店 | 去哪儿/携程/飞猪查询 |
| `ai-agent-wars` | AI Agent竞争 | 2026 AI Agent平台分析 |
| `solo-company-crew` | 一人公司、solo | 一人公司Agent团队 |

---

## 四、使用方法

### 4.1 日常使用

直接在对话中说出触发词即可，系统自动匹配Skill加载。例如：

```
"分析一下黄金XAUUSD"        → 自动触发 trading-analysis
"执行帝意日报"              → 自动触发 diyi-daily
"发公众号"                  → 自动触发 wechat-publisher
"深度调研XX"                → 自动触发 deep-research
"回测VolBreak"              → 自动触发 volbreak-backtest
```

### 4.2 迁移到新机器

1. 复制 `~/.workbuddy/skills/` 整个目录到新机器同路径
2. 复制 `~/.workbuddy/mcp.json` 到新机器同路径
3. 复制 `~/.workbuddy/MEMORY.md` 到新机器同路径
4. 复制 `~/.workbuddy/SOUL.md` + `IDENTITY.md` + `USER.md`
5. 新机器打开 WorkBuddy 即可使用全部Skill和MCP

**一键迁移命令（在新机器执行）**：
```bash
# 假设旧机器文件已复制到 U盘/网络共享
cp -r skills/ ~/.workbuddy/skills/
cp mcp.json ~/.workbuddy/mcp.json
cp MEMORY.md ~/.workbuddy/MEMORY.md
```

### 4.3 查阅兵器库

说"兵器库"或"skill索引"即可加载本Skill，查看全部可用Skill列表。

### 4.4 添加新Skill

1. 说"创建skill"触发 `skill-creator`
2. 编写SKILL.md放入 `~/.workbuddy/skills/<skill-name>/`
3. 更新本兵器库索引

---

## 五、统计

| 维度 | 数量 |
|------|------|
| 通神核心 | 7 |
| 交易/量化 | 7 |
| 内容/公众号 | 12 |
| 浏览器/自动化 | 4 |
| 视频/图像 | 5 |
| 研究/数据 | 5 |
| 开发/部署 | 6 |
| GitHub工具 | 5 |
| AI/Coze | 3 |
| 小说/创作 | 4 |
| 工具类 | 15 |
| 其他 | 5 |
| **合计有用Skill** | **78** |
| MCP服务器 | 10 |
| API凭证 | 5 |

---

## 六、维护规则

1. 新增Skill后必须更新本索引
2. API Key变更后必须同步更新 mcp.json + MEMORY.md + 本文件
3. GitHub PAT 2027-06-15到期，已设2027-06-01提醒
4. 本文件为通神系统唯一Skill索引权威来源

---

*通神兵器库 v1.0 — 2026-06-21 封存*
*天枢居中调度，五行各司其职。兵器库一键封存，迁移无忧。*
