# 通神认证Agent - 使用说明

## 📖 概述

通神认证Agent是一个融合了78个专业技能的AI系统，支持自优化进化。它集成了通神兵器库的所有功能，能够处理从交易分析到内容创作的各种任务。

## 🚀 快速开始

### 1. 环境要求

- Node.js >= 16.0.0
- npm >= 8.0.0
- Windows 10/11 或 Linux/macOS

### 2. 部署步骤

#### 方法一：使用部署脚本（推荐）

```bash
# 1. 进入目录
cd C:\Users\Administrator\Desktop\通神兵器库

# 2. 运行部署脚本
node deploy-to-claude.js
```

#### 方法二：手动部署

```bash
# 1. 安装依赖
npm install

# 2. 复制配置文件
cp configs/example.json configs/tongshen.json

# 3. 启动服务
node core-scheduler.js
```

### 3. 验证部署

```bash
# 运行测试脚本
node test.js
```

## 🎯 核心功能

### 1. 78个技能集成

| 分类 | 数量 | 示例技能 |
|------|------|----------|
| 通神核心 | 7 | tongshen-v8.1、反截断、自进化 |
| 交易/量化 | 7 | 金价分析、VolBreak回测、自动交易 |
| 内容/公众号 | 12 | 公众号发布、帝意日报、视频生成 |
| 研究/数据 | 5 | 深度调研、宏观数据、AI搜索 |
| 开发/部署 | 6 | 网站部署、GitHub Pages、Vercel |
| 工具类 | 15 | 文件转换、图片生成、安全审计 |
| 其他 | 18 | 浏览器自动化、视频图像、GitHub工具 |

### 2. 智能调度系统

- **M0元认知**：自我反思、策略规划、任务分解
- **7域路由**：自动识别并路由到最适合的技能
- **链式执行**：绕过输出限制，分步完成任务

### 3. 自优化进化

- **性能监控**：实时跟踪技能执行效果
- **进化周期**：每分钟自动优化策略
- **自适应学习**：根据使用模式调整配置
- **自动升级**：技能版本自动更新

## 💡 使用方法

### 1. 直接触发

在对话中直接说出技能触发词：

```bash
"分析一下黄金XAUUSD"        → 触发 trading-analysis
"执行帝意日报"              → 触发 diyi-daily
"发公众号"                  → 触发 wechat-publisher
"深度调研XX"                → 触发 deep-research
"回测VolBreak策略"          → 触发 volbreak-backtest
```

### 2. 组合使用

系统会自动选择最适合的技能组合：

```bash
"分析市场并发布报告"        → trading-analysis + wechat-publisher
"创建一个完整的营销方案"    → 自动分解为多个子任务
```

### 3. API调用

通过HTTP API使用：

```bash
# 获取技能列表
curl http://localhost:3000/skills

# 查找技能
curl "http://localhost:3000/skills/find?trigger=黄金"

# 执行技能
curl -X POST http://localhost:3000/execute \
  -H "Content-Type: application/json" \
  -d '{"skill": "trading-analysis", "context": {"symbol": "XAUUSD"}}'

# 获取统计信息
curl http://localhost:3000/stats
```

## 📁 文件结构

```
通神兵器库/
├── auth-agent-core.js      # 认证Agent核心
├── core-scheduler.js        # 核心调度器
├── server.js               # Web服务器
├── deploy-to-claude.js      # 部署脚本
├── test.js                 # 测试脚本
├── README.md               # 使用说明
├── SKILL.md               # 技能索引
├── configs/               # 配置文件
│   ├── tongshen-integration.json  # 集成配置
│   └── mcp-integrated.json        # MCP配置
├── skills/                # 技能目录
│   └── index.json         # 技能索引
├── logs/                  # 日志文件
│   └── tongshen.log      # 主日志
├── core/                  # 核心文件副本
│   ├── auth-agent-core.js
│   └── core-scheduler.js
└── backup/               # 备份文件
```

## ⚙️ 配置说明

### 1. 主配置文件 (configs/tongshen-integration.json)

```json
{
  "version": "2.0.0",
  "name": "通神认证Agent",
  "description": "融合78个技能的认证Agent系统",
  "skills": {
    "path": "D:\\WorkBuddy",
    "autoLoad": true,
    "categories": [...]
  },
  "mcp": {
    "enabled": true,
    "servers": [...]
  },
  "evolution": {
    "enabled": true,
    "interval": 60000,
    "maxGenerations": 100
  }
}
```

### 2. 环境变量 (.env)

```env
TONGSHEN_AGENT_ENABLED=true
TONGSHEN_AGENT_PATH=C:\Users\Administrator\Desktop\通神兵器库
TONGSHEN_SKILLS_PATH=D:\WorkBuddy
TONGSHEN_EVOLUTION_ENABLED=true
TONGSHEN_EVOLUTION_INTERVAL=60000
MCP_FIRECRAWL_KEY=fc-7f6c51167e4d4c4abe925b8d179ae30d
MCP_GITHUB_TOKEN=ghp_YOUR_TOKEN_PLACEHOLDER
```

## 🔧 高级功能

### 1. 性能监控

查看系统运行状态：

```bash
# 获取详细统计
curl http://localhost:3000/stats

# 导出配置
curl http://localhost:3000/export > config-export.json

# 手动触发优化
curl -X POST http://localhost:3000/optimize
```

### 2. 日志管理

日志文件位置：

- 主日志: `logs/tongshen.log`
- 错误日志: `logs/error.log`
- 访问日志: `logs/access.log`

查看最新日志：

```bash
tail -f logs/tongshen.log
```

### 3. 技能管理

#### 添加新技能

1. 创建技能目录
2. 编写SKILL.md文件
3. 更新索引
4. 重启服务

#### 禁用/启用技能

编辑配置文件中的技能状态：

```json
{
  "enabled": true,
  "skills": {
    "trading-analysis": {
      "enabled": false
    }
  }
}
```

## 🐛 故障排除

### 1. 常见问题

#### 技能加载失败

**问题**: 技能无法加载
**解决**:
- 检查技能路径是否正确
- 确认SKILL.md文件格式正确
- 查看日志中的错误信息

#### MCP连接失败

**问题**: MCP服务器无法连接
**解决**:
- 检查网络连接
- 验证API凭证是否正确
- 重启MCP服务

#### 任务执行失败

**问题**: 任务执行返回错误
**解决**:
- 检查输入参数
- 查看技能依赖是否满足
- 检查资源权限

### 2. 重启服务

```bash
# 使用PM2重启
pm2 reload tongshen-auth-agent

# 或直接重启
node core-scheduler.js
```

### 3. 回滚部署

如果部署出现问题，可以使用备份文件回滚：

```bash
# 恢复claude.md
cp backup/claude.md.2024-01-01.backup claude.md

# 恢复配置
cp backup/config.json.2024-01-01.backup config.json
```

## 📊 性能优化

### 1. 调整优化参数

在配置文件中调整：

```json
{
  "evolution": {
    "interval": 30000,  // 减少到30秒
    "maxGenerations": 50  // 减少进化代数
  }
}
```

### 2. 技能优先级

系统会自动调整技能优先级，也可以手动设置：

```json
{
  "skills": {
    "trading-analysis": {
      "priority": 9  // 最高优先级
    }
  }
}
```

### 3. 缓存优化

启用技能缓存以提高响应速度：

```json
{
  "cache": {
    "enabled": true,
    "ttl": 3600,  // 1小时缓存
    "maxSize": 100  // 最大缓存数量
  }
}
```

## 🔐 安全注意事项

1. **API凭证安全**
   - 不要在代码中硬编码API密钥
   - 使用环境变量或密钥管理服务
   - 定期轮换API密钥

2. **文件权限**
   - 限制技能目录的写入权限
   - 定期备份重要配置
   - 监控异常文件操作

3. **网络安全**
   - 使用HTTPS加密传输
   - 实施访问控制
   - 监控异常请求

## 🤝 贡献指南

欢迎贡献新技能或改进现有功能：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

### 技能开发规范

1. 创建SKILL.md文件，包含必要信息
2. 实现execute函数
3. 添加适当的错误处理
4. 编写单元测试

## 📞 支持

如有问题或建议，请：

1. 查看日志文件
2. 运行测试脚本
3. 查看GitHub Issues
4. 联系开发团队

## 📈 更新日志

### v2.0.0 (2024-01-01)
- 集成78个技能
- 实现自优化进化
- 完整的API接口
- 增强的监控功能

### v1.0.0 (2023-12-01)
- 初始版本发布
- 基础技能集成
- 简单的调度功能

---

*通神认证Agent - 让AI系统不断进化*