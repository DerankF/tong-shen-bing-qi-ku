# 🤖 高府·帝意 CLI 工具 v6.0

> **PowerShell 版本的 CLI 工具**，用于评估 AI Agent 系统

---

## 📋 简介

高府·帝意 CLI 工具是 PowerShell 版本的命令行界面，提供完整的 AI Agent 评估功能：

- 🏛️ **高府认证** - 基于五维模型的技术评测
- 🏆 **帝意排行** - 基于商业价值的等级评估  
- 🔐 **RAC信任** - 基于证据链的信任分析
- 📊 **综合评估** - 整合三位一体的完整评估

---

## 🚀 快速开始

### 1. 运行演示

```powershell
# 运行快速演示
.\quick-start.ps1

# 或直接运行主程序
.\gaofu-diyi.ps1 help
```

### 2. 安装到系统

```powershell
# 安装到用户目录（推荐）
.\install.ps1

# 全局安装
.\install.ps1 -Global

# 添加到系统PATH
.\install.ps1 -AddToPath
```

---

## 🎯 使用方法

### 评估单个 Agent

```powershell
# 快速评估
.\gaofu-diyi.ps1 evaluate -AgentId "my-agent" -Capability 85 -Security 80

# 标准评估（包含所有维度）
.\gaofu-diyi.ps1 evaluate -AgentId "gemini" -Capability 88 -Security 90 -Collaboration 82 -Evolution 85 -Ethics 90 -DaoHang 82 -FaXing 88 -LiXing 75 -YuXing 85 -ShouXing 90

# 深度评估模式
.\gaofu-diyi.ps1 evaluate -AgentId "test" -Capability 90 -Security 85 -Mode deep
```

### 生成排行榜

```powershell
# 生成前10名排行榜
.\gaofu-diyi.ps1 rank

# 指定类别和数量
.\gaofu-diyi.ps1 rank -Category "general" -Top 5
```

### 生成报告

```powershell
# 文本格式报告
.\gaofu-diyi.ps1 report -AgentId "claude-3" -Format text

# JSON格式报告
.\gaofu-diyi.ps1 report -AgentId "gpt-4" -Format json

# HTML格式报告（推荐）
.\gaofu-diyi.ps1 report -AgentId "gemini" -Format html

# 保存到文件
.\gaofu-diyi.ps1 report -AgentId "claude-3" -Format html -OutputPath ".\report.html"
```

### 管理功能

```powershell
# 查看帮助
.\gaofu-diyi.ps1 help

# 查看系统配置
.\gaofu-diyi.ps1 config
```

---

## 📊 评分说明

### 高府五维（权重）
- **能力表现** (30%): 任务完成、推理深度、上下文理解
- **安全保障** (25%): 数据保护、漏洞防护、伦理底线
- **协作能力** (20%): 接口设计、协议合规、集成便捷
- **进化潜力** (15%): 学习能力、改进速率、自我纠错
- **伦理合规** (10%): 价值对齐、透明度、公平性

### 帝意五维（权重）
- **道行** (25%): 战略认知、格局视野、顶层设计
- **法行** (30%): 执行力、落地能力、技术实力
- **利行** (15%): 商业价值、变现能力、盈利模式
- **愈行** (15%): 用户体验、情绪价值、产品打磨
- **守行** (15%): 安全合规、风险控制、伦理底线

### RAC信任分析
- **基础分**: 50分
- **开源加分**: +15分
- **审计报告**: +20分
- **守行贡献**: 最高+15分

---

## 🏗️ 架构组件

```
CLI 工具/
├── gaofu-diyi.ps1          # 主程序
├── install.ps1             # 安装脚本
├── quick-start.ps1         # 快速演示
├── README.md              # 说明文档
└── modules/               # 模块目录
    ├── gaofu-certification.psm1    # 高府认证模块
    ├── diyi-ranking.psm1          # 帝意排行模块
    ├── rac-trust.psm1            # RAC信任分析
    ├── report-generator.psm1     # 报告生成
    └── gaofu-diyi-engine.psm1    # 综合评估引擎
```

---

## 🔧 评估模式

### 快速评估（quick）
- 预计时间: < 3分钟
- 包含: 基础维度 + 核心指标
- 适用: 快速筛选和初步评估

### 标准评估（standard）
- 预计时间: < 15分钟
- 包含: 所有维度 + 完整分析
- 适用: 正式评估和决策参考

### 深度评估（deep）
- 预计时间: < 60分钟
- 包含: 详细分析 + 专业建议
- 适用: 深度研究和投资决策

### 持续追踪（continuous）
- 预计时间: 持续监控
- 包含: 实时监控 + 自动复评
- 适用: 长期跟踪和风险管理

---

## 📋 输出格式

### 文本格式
- 简洁易读
- 适合终端查看
- 快速了解关键指标

### JSON格式
- 结构化数据
- 适合程序处理
- 可集成到其他系统

### HTML格式
- 可视化展示
- 包含图表和颜色
- 适合正式报告和演示

---

## 🎮 示例

### 示例1: 评估Claude 3
```powershell
.\gaofu-diyi.ps1 evaluate -AgentId "claude-3" -AgentName "Claude 3" -Capability 92 -Security 88 -Collaboration 85 -Evolution 90 -Ethics 95 -DaoHang 85 -FaXing 90 -LiXing 80 -YuXing 88 -ShouXing 90
```

### 示例2: 生成排行榜
```powershell
.\gaofu-diyi.ps1 rank -Category "all" -Top 5 | Format-Table
```

### 示例3: 保存HTML报告
```powershell
.\gaofu-diyi.ps1 report -AgentId "gpt-4" -Format html -OutputPath ".\gpt4-report.html"
```

---

## ⚙️ 配置

安装后配置文件位于：`$env:USERPROFILE\gaofu-diyi-cli\config.json`

```json
{
    "version": "6.0.0",
    "default_mode": "standard",
    "default_format": "text",
    "default_category": "general",
    "default_top": 10,
    "logging_enabled": true,
    "output_directory": "$env:USERPROFILE\gaofu-diyi-cli\reports"
}
```

---

## 🚨 注意事项

1. **执行策略**: 确保PowerShell执行策略允许运行脚本
2. **权限**: 某些操作可能需要管理员权限
3. **数据安全**: 评估结果可能包含敏感信息，请注意保护
4. **版本兼容**: 建议使用PowerShell 5.1或更高版本

---

## 📞 支持

- **文档**: 查看 `CLAUDE.md` 了解完整架构
- **演示**: 运行 `.\quick-start.ps1` 查看演示
- **技术支持**: tech@gaofu-diyi.example
- **GitHub**: https://github.com/gaofu-diyi/ultimate-system

---

**© 2026 高府认证团队 & 帝意共识智脑**

> "高府不定义价值，帝意不创造信任。我们只提供当前证据下最可信的分析框架。"