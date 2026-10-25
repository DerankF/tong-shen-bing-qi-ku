# 通神认证Agent - 项目文件清单

## 📁 完整文件结构

```
通神兵器库/
├── 🔧 核心代码文件
│   ├── auth-agent-core.js      # 认证Agent核心系统
│   ├── core-scheduler.js        # 核心调度器
│   └── server.js               # Web服务器
│
├── 🚀 部署和配置文件
│   ├── deploy-to-claude.js     # 部署到Claude底层的脚本
│   ├── setup-repo.bat          # Windows创建仓库脚本
│   ├── setup-repo.ps1          # PowerShell创建仓库脚本
│   ├── setup-pages.ps1         # 配置GitHub Pages脚本
│   ├── start.sh                # Unix启动脚本
│   └── start.bat               # Windows启动脚本
│
├── 📚 文档文件
│   ├── README.md               # 基础使用说明
│   ├── README_GITHUB.md       # GitHub仓库说明
│   ├── PROJECT_FILES.md        # 项目文件清单（本文件）
│   ├── DEPLOYMENT_CHECKLIST.md # 部署检查清单
│   ├── claude-integrated.md   # Claude集成设计
│   └── SKILL.md               # 技能索引
│
├── ⚙️ 配置文件
│   ├── configs/
│   │   ├── tongshen-integration.json  # 集成配置
│   │   └── mcp-integrated.json        # MCP配置
│   ├── .env.example            # 环境变量模板
│   ├── .gitignore              # Git忽略规则
│   └── .gitattributes          # Git属性配置
│
├── 📊 测试和工具文件
│   ├── test.js                 # 测试脚本
│   ├── create-github-repo.js   # 创建GitHub仓库脚本
│   └── create-repo.ps1         # PowerShell创建仓库脚本
│
├── 📄 许可证
│   └── LICENSE                 # MIT许可证
│
└── 📝 其他
    └── 78个技能文件           # 来自D:\WorkBuddy
```

## 📋 文件说明

### 🔧 核心代码文件

#### auth-agent-core.js
- **功能**: 认证Agent核心系统
- **包含**: 78个技能集成、动态加载、自优化进化
- **关键特性**:
  - 技能管理系统
  - 性能监控
  - 自优化算法
  - API凭证管理

#### core-scheduler.js
- **功能**: 核心调度器
- **包含**: M0元认知、7域路由、链式执行
- **关键特性**:
  - 元认知模块
  - 智能路由系统
  - 任务链管理
  - 技能匹配算法

#### server.js
- **功能**: Web服务器
- **包含**: RESTful API、管理界面、实时监控
- **关键特性**:
  - 技能管理API
  - 性能统计API
  - 配置导出/导入
  - WebSocket实时更新

### 🚀 部署和配置文件

#### deploy-to-claude.js
- **功能**: 部署到Claude底层
- **包含**: 环境检查、配置备份、系统集成
- **关键特性**:
  - 自动化部署流程
  - 配置文件集成
  - 测试验证
  - 回滚机制

#### setup-repo.bat / setup-repo.ps1
- **功能**: 创建GitHub仓库
- **包含**: Git初始化、文件提交、远程推送
- **关键特性**:
  - 环境检查
  - 自动化流程
  - 错误处理
  - 用户交互

#### setup-pages.ps1
- **功能**: 配置GitHub Pages
- **包含**: 创建gh-pages分支、部署网站
- **关键特性**:
  - 自动创建页面
  - 响应式设计
   - API状态检查
   - 定时更新

### 📚 文档文件

#### README.md
- **用途**: 项目基础使用说明
- **包含**: 快速开始、配置说明、使用方法

#### README_GITHUB.md
- **用途**: GitHub仓库详细说明
- **包含**: 功能介绍、架构图、API文档、贡献指南

#### DEPLOYMENT_CHECKLIST.md
- **用途**: 部署检查清单
- **包含**: 完成功能、部署步骤、问题解决方案

#### claude-integrated.md
- **用途**: Claude集成设计文档
- **包含**: 系统架构、实施步骤、未来规划

#### SKILL.md
- **用途**: 技能索引
- **包含**: 78个技能完整列表、分类、触发词

### ⚙️ 配置文件

#### configs/tongshen-integration.json
- **用途**: 集成配置
- **包含**: 技能路径、MCP设置、进化参数

#### configs/mcp-integrated.json
- **用途**: MCP服务器配置
- **包含**: 10个MCP服务器配置、API凭证

#### .env.example
- **用途**: 环境变量模板
- **包含**: 所有必要的环境变量配置

#### .gitignore
- **用途**: Git忽略规则
- **包含**: Node.js、日志、临时文件等

#### .gitattributes
- **用途**: Git属性配置
- **包含**: 行尾符处理、二进制文件处理

### 📊 测试和工具文件

#### test.js
- **功能**: 系统测试脚本
- **包含**: 功能测试、性能测试、错误测试

#### create-github-repo.js
- **功能**: Node.js版创建仓库脚本
- **包含**: API调用、自动创建、错误处理

## 🎯 78个技能列表

### 通神核心 (7个)
1. tongshen-v8.1 - 全域调度核心
2. tongshen-anti-truncation - 反截断机制
3. tongshen-team-dispatch - 团队调度
4. self-evolution - 系统自进化
5. info-compressor - 信息压缩
6. task-chain - 任务链管理
7. dmp-skill-logger - 任务历史记录

### 交易/量化 (7个)
8. trading-analysis - 金价分析
9. volbreak-backtest - 回测引擎
10. volbreak-auto-trading - 自动交易
11. vb-pro-btceth-detection - BTC/ETH检测
12. xauusd-daily-strategy - 黄金策略
13. mt5-swing-trader-system - MT5摇摆交易
14. wallstreet-trading-closed-loop - 交易闭环

### 内容/公众号 (12个)
15. wechat-publisher - 公众号发布
16. diyi-daily - 帝意日报
17. diyi-intro-video - 品牌介绍视频
18. diyi-video-producer - 视频生产
19. weixin-article-writer - 财经文章
20. content-factory-pipeline - 内容流水线
21. explosive-cover-generator-gzh - 封面设计
22. daily-batch-publisher - 批量发布
23. wechat-article-search - 文章搜索
24. wechat-article-pro - 文章专业版
25. wechat-viral-topic - 爆款选题
26. khazix-writer - 公众号长文

### 研究/数据 (5个)
27. deep-research - 深度调研
28. hot - 热搜数据
29. macro-monitor - 宏观监控
30. perplexity - AI搜索
31. multi-search-engine - 多引擎搜索

### 开发/部署 (6个)
32. deploy-website - 网站部署
33. ui-new - UI界面设计
34. web-deploy - Web部署
35. html-deploy - HTML部署
36. vercel-deploy - Vercel部署
37. github-pages-auto-deploy - GitHub Pages部署

### 工具类 (15个)
38. md-to-pdf-cjk - MD转PDF
39. markitdown-skill - 文件转换
40. summarize - 摘要生成
41. canvas-design - 设计生成
42. humanizer - 去AI化处理
43. openai-image-gen - 图片生成
44. nano-banana-pro - 图片编辑
45. gifgrep - GIF搜索
46. skills-security-check - 安全审计
47. skill-creator - 技能创建
48. paper-quick-reader - 论文速读
49. web-access - 网络访问
50. obsidian - 笔记管理
51. gmail - 邮件集成
52. lark-unified - 飞书集成

### 其他 (18个)
53. 浏览器/自动化 (4个)
54. 视频/图像 (5个)
55. GitHub工具 (5个)
56. AI/Coze (3个)
57. 小说/创作 (4个)
58. 其他 (5个)

## 📝 使用说明

### 1. 创建GitHub仓库

```bash
# 方法一：使用PowerShell脚本（推荐）
./setup-repo.ps1

# 方法二：使用批处理脚本
setup-repo.bat

# 方法三：使用Node.js脚本
node create-github-repo.js
```

### 2. 配置GitHub Pages

```bash
# 配置GitHub Pages网站
./setup-pages.ps1
```

### 3. 部署到Claude

```bash
# 部署到Claude底层
node deploy-to-claude.js
```

### 4. 运行测试

```bash
# 运行系统测试
node test.js
```

### 5. 启动服务

```bash
# Windows
start.bat

# Linux/macOS
./start.sh
```

## 🔗 相关链接

- [GitHub仓库](https://github.com/your-username/tongshen-auth-agent)
- [GitHub Pages](https://your-username.github.io/tongshen-auth-agent)
- [API文档](https://github.com/your-username/tongshen-auth-agent#api)
- [问题反馈](https://github.com/your-username/tongshen-auth-agent/issues)

---

*最后更新: 2024-01-01*