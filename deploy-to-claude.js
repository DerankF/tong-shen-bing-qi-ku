#!/usr/bin/env node

/**
 * 通神认证Agent部署脚本
 * 用于将通神系统集成到Claude底层
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class ClaudeDeployment {
    constructor() {
        this.projectRoot = process.cwd();
        this.backupDir = path.join(this.projectRoot, 'backup');
        this.deploymentDate = new Date().toISOString().split('T')[0];
        this.config = {
            overwrite: false,
            backup: true,
            test: true,
            verbose: true
        };
    }

    /**
     * 执行部署
     */
    async deploy() {
        console.log('🚀 开始部署通神认证Agent到Claude底层');
        console.log(`部署日期: ${this.deploymentDate}`);
        console.log('部署配置:', this.config);

        try {
            // 1. 检查环境
            await this.checkEnvironment();

            // 2. 备份现有配置
            if (this.config.backup) {
                await this.backupExistingConfig();
            }

            // 3. 部署核心文件
            await this.deployCoreFiles();

            // 4. 集成到Claude系统
            await this.integrateWithClaude();

            // 5. 配置MCP服务器
            await this.configureMCP();

            // 6. 部署技能文件
            await this.deploySkills();

            // 7. 创建启动脚本
            await this.createStartupScripts();

            // 8. 测试部署
            if (this.config.test) {
                await this.testDeployment();
            }

            console.log('✅ 部署完成！');
            return true;

        } catch (error) {
            console.error('❌ 部署失败:', error.message);
            await this.rollback();
            return false;
        }
    }

    /**
     * 检查环境
     */
    async checkEnvironment() {
        console.log('🔍 检查部署环境...');

        // 检查Node.js版本
        const nodeVersion = process.version;
        console.log(`Node.js版本: ${nodeVersion}`);

        // 检查Claude CLI是否安装
        try {
            const claudeVersion = execSync('claude --version', { encoding: 'utf8' });
            console.log(`Claude CLI版本: ${claudeVersion.trim()}`);
        } catch (error) {
            console.warn('警告: Claude CLI未安装');
        }

        // 检查必要的目录
        const requiredDirs = ['skills', 'configs', 'logs'];
        for (const dir of requiredDirs) {
            const dirPath = path.join(this.projectRoot, dir);
            if (!fs.existsSync(dirPath)) {
                fs.mkdirSync(dirPath, { recursive: true });
                console.log(`创建目录: ${dir}`);
            }
        }

        // 检查D盘技能目录
        const skillDirs = [
            'D:\\WorkBuddy',
            'D:\\通神兵器库',
            'D:\\安装位置\\WORKbuddy'
        ];

        this.existingSkillDirs = [];
        for (const dir of skillDirs) {
            if (fs.existsSync(dir)) {
                this.existingSkillDirs.push(dir);
                console.log(`✅ 找到技能目录: ${dir}`);
            }
        }

        if (this.existingSkillDirs.length === 0) {
            throw new Error('未找到任何技能目录');
        }
    }

    /**
     * 备份现有配置
     */
    async backupExistingConfig() {
        console.log('💾 备份现有配置...');

        if (!fs.existsSync(this.backupDir)) {
            fs.mkdirSync(this.backupDir, { recursive: true });
        }

        // 备份claude.md
        const claudeMdPath = path.join(this.projectRoot, 'claude.md');
        if (fs.existsSync(claudeMdPath)) {
            const backupPath = path.join(this.backupDir, `claude.md.${this.deploymentDate}.backup`);
            fs.copyFileSync(claudeMdPath, backupPath);
            console.log(`备份claude.md到: ${backupPath}`);
        }

        // 备份配置文件
        const configPath = path.join(this.projectRoot, 'config.json');
        if (fs.existsSync(configPath)) {
            const backupPath = path.join(this.backupDir, `config.json.${this.deploymentDate}.backup`);
            fs.copyFileSync(configPath, backupPath);
            console.log(`备份config.json到: ${backupPath}`);
        }
    }

    /**
     * 部署核心文件
     */
    async deployCoreFiles() {
        console.log('📦 部署核心文件...');

        // 复制核心文件到目标位置
        const coreFiles = [
            'auth-agent-core.js',
            'core-scheduler.js',
            'server.js'
        ];

        for (const file of coreFiles) {
            const sourcePath = path.join(this.projectRoot, file);
            const destPath = path.join(this.projectRoot, 'core', file);

            if (fs.existsSync(sourcePath)) {
                fs.copyFileSync(sourcePath, destPath);
                console.log(`部署核心文件: ${file}`);
            }
        }

        // 创建集成配置
        const integrationConfig = {
            version: '2.0.0',
            name: '通神认证Agent',
            description: '融合78个技能的认证Agent系统',
            skills: {
                path: 'D:\\WorkBuddy',
                autoLoad: true,
                categories: [
                    '通神核心',
                    '交易/量化',
                    '内容/公众号',
                    '研究/数据',
                    '开发/部署',
                    '工具类'
                ]
            },
            mcp: {
                enabled: true,
                servers: [
                    'filesystem',
                    'github',
                    'fetch',
                    'memory',
                    'sequential-thinking',
                    'puppeteer',
                    'context7',
                    'firecrawl',
                    'playwright',
                    'sqlite'
                ]
            },
            evolution: {
                enabled: true,
                interval: 60000,
                maxGenerations: 100
            }
        };

        const configPath = path.join(this.projectRoot, 'configs', 'tongshen-integration.json');
        fs.writeFileSync(configPath, JSON.stringify(integrationConfig, null, 2));
        console.log(`创建集成配置: ${configPath}`);
    }

    /**
     * 集成到Claude系统
     */
    async integrateWithClaude() {
        console.log('🔗 集成到Claude系统...');

        // 查找claude.md文件
        const claudeMdPath = path.join(this.projectRoot, 'claude.md');
        let claudeMd = '';

        if (fs.existsSync(claudeMdPath)) {
            claudeMd = fs.readFileSync(claudeMdPath, 'utf8');
        }

        // 创建通神集成章节
        const tongshenIntegration = `
## 通神认证Agent集成

### 系统概述
通神认证Agent已深度集成到Claude底层，提供了78个专业技能的访问能力，并支持自优化进化。

### 核心能力
- **M0元认知**：自我反思、策略规划、任务分解
- **7域路由**：自动识别并路由到最适合的技能
- **链式执行**：绕过输出限制，分步完成任务
- **自优化进化**：持续学习和改进系统性能

### 可用技能分类
1. **通神核心** (7个)
   - tongshen-v8.1：全域调度核心
   - tongshen-anti-truncation：反截断机制
   - tongshen-team-dispatch：团队调度
   - self-evolution：系统自进化
   - info-compressor：信息压缩
   - task-chain：任务链管理
   - dmp-skill-logger：任务历史记录

2. **交易/量化** (7个)
   - trading-analysis：金价分析
   - volbreak-backtest：回测引擎
   - volbreak-auto-trading：自动交易
   - vb-pro-btceth-detection：BTC/ETH检测
   - xauusd-daily-strategy：黄金策略
   - mt5-swing-trader-system：MT5摇摆交易
   - wallstreet-trading-closed-loop：交易闭环

3. **内容/公众号** (12个)
   - wechat-publisher：公众号发布
   - diyi-daily：帝意日报
   - diyi-intro-video：品牌介绍视频
   - diyi-video-producer：视频生产
   - weixin-article-writer：财经文章
   - content-factory-pipeline：内容流水线
   - explosive-cover-generator-gzh：封面设计
   - daily-batch-publisher：批量发布
   - wechat-article-search：文章搜索
   - wechat-article-pro：文章专业版
   - wechat-viral-topic：爆款选题
   - khazix-writer：公众号长文

4. **研究/数据** (5个)
   - deep-research：深度调研
   - hot：热搜数据
   - macro-monitor：宏观监控
   - perplexity：AI搜索
   - multi-search-engine：多引擎搜索

5. **开发/部署** (6个)
   - deploy-website：网站部署
   - ui-new：UI界面设计
   - web-deploy：Web部署
   - html-deploy：HTML部署
   - vercel-deploy：Vercel部署
   - github-pages-auto-deploy：GitHub Pages部署

6. **工具类** (15个)
   - md-to-pdf-cjk：MD转PDF
   - markitdown-skill：文件转换
   - summarize：摘要生成
   - canvas-design：设计生成
   - humanizer：去AI化处理
   - openai-image-gen：图片生成
   - nano-banana-pro：图片编辑
   - gifgrep：GIF搜索
   - skills-security-check：安全审计
   - skill-creator：技能创建
   - paper-quick-reader：论文速读
   - web-access：网络访问
   - obsidian：笔记管理
   - gmail：邮件集成
   - lark-unified：飞书集成

7. **其他** (18个)
   - 浏览器/自动化：4个
   - 视频/图像：5个
   - GitHub工具：5个
   - AI/Coze：3个
   - 小说/创作：4个
   - 其他：5个

### 使用方法
1. **直接触发**：在对话中说出技能触发词
   - "分析黄金XAUUSD" → trading-analysis
   - "发公众号" → wechat-publisher
   - "深度调研XX" → deep-research

2. **组合使用**：系统会自动选择最适合的技能组合
   - "分析并发布市场报告" → trading-analysis + wechat-publisher

3. **元认知调度**：复杂任务会自动分解
   - "创建一个完整的营销方案" → 自动分解为多个子任务

### 自优化特性
- **性能监控**：实时跟踪每个技能的执行效果
- **进化周期**：每分钟自动优化技能策略
- **自适应学习**：根据使用模式调整触发词和配置
- **自动升级**：技能版本自动更新

### 配置说明
主要配置文件位于 \`configs/tongshen-integration.json\`，包含：
- 技能路径配置
- MCP服务器设置
- 进化参数
- 性能阈值

### 监控和维护
- 日志文件：\`logs/tongshen.log\`
- 性能统计：\`stats/performance.json\`
- 健康检查：\`health/status.json\`

### 故障处理
如果遇到问题，请检查：
1. 技能文件路径是否正确
2. MCP服务器连接状态
3. API凭证是否有效
4. 系统日志中的错误信息
`;

        // 如果claude.md不存在，创建新文件
        if (!fs.existsSync(claudeMdPath)) {
            claudeMd = `# Claude + 通神认证Agent 集成系统\n\n${tongshenIntegration}`;
        } else {
            // 如果存在，添加集成章节
            const integrationSection = tongshenIntegration;
            claudeMd += `\n\n${integrationSection}`;
        }

        fs.writeFileSync(claudeMdPath, claudeMd);
        console.log(`更新claude.md，添加通神集成章节`);
    }

    /**
     * 配置MCP服务器
     */
    async configureMCP() {
        console.log('⚙️ 配置MCP服务器...');

        // 创建MCP配置文件
        const mcpConfig = {
            mcpServers: {
                filesystem: {
                    command: "npx",
                    args: [
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        "C:\\Users\\Administrator\\Desktop\\通神兵器库"
                    ],
                    disabled: false
                },
                github: {
                    disabled: false,
                    timeout: 60,
                    type: "stdio",
                    command: "npx",
                    args: [
                        "-y",
                        "@modelcontextprotocol/server-github"
                    ],
                    env: {
                        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_YOUR_TOKEN_PLACEHOLDER"
                    }
                },
                fetch: {
                    command: "cmd",
                    args: [
                        "/c",
                        "npx",
                        "-y",
                        "@modelcontextprotocol/server-fetch"
                    ],
                    disabled: false
                },
                memory: {
                    command: "cmd",
                    args: [
                        "/c",
                        "npx",
                        "-y",
                        "@modelcontextprotocol/server-memory"
                    ],
                    disabled: false
                },
                sequential-thinking: {
                    command: "cmd",
                    args: [
                        "/c",
                        "npx",
                        "-y",
                        "@modelcontextprotocol/server-sequential-thinking"
                    ],
                    disabled: false
                },
                puppeteer: {
                    command: "cmd",
                    args: [
                        "/c",
                        "npx",
                        "-y",
                        "@modelcontextprotocol/server-puppeteer"
                    ],
                    disabled: false
                },
                context7: {
                    command: "cmd",
                    args: [
                        "/c",
                        "npx",
                        "-y",
                        "@upstash/context7-mcp"
                    ],
                    disabled: false
                },
                firecrawl: {
                    command: "npx",
                    args: [
                        "-y",
                        "firecrawl-mcp"
                    ],
                    env: {
                        "FIRECRAWL_API_KEY": "fc-7f6c51167e4d4c4abe925b8d179ae30d"
                    },
                    disabled: false
                },
                playwright: {
                    command: "npx",
                    args: [
                        "-y",
                        "@playwright/mcp@latest"
                    ],
                    disabled: false
                },
                sqlite: {
                    command: "npx",
                    args: [
                        "-y",
                        "@modelcontextprotocol/server-sqlite",
                        "C:\\Users\\Administrator\\workspace\\trading.db"
                    ],
                    disabled: false
                }
            }
        };

        const mcpPath = path.join(this.projectRoot, 'configs', 'mcp-integrated.json');
        fs.writeFileSync(mcpPath, JSON.stringify(mcpConfig, null, 2));
        console.log(`创建MCP配置: ${mcpPath}`);

        // 创建系统环境变量配置
        const envConfig = {
            TONGSHEN_AGENT_ENABLED: true,
            TONGSHEN_AGENT_PATH: "C:\\Users\\Administrator\\Desktop\\通神兵器库",
            TONGSHEN_SKILLS_PATH: "D:\\WorkBuddy",
            TONGSHEN_EVOLUTION_ENABLED: true,
            TONGSHEN_EVOLUTION_INTERVAL: 60000,
            MCP_FIRECRAWL_KEY: "fc-7f6c51167e4d4c4abe925b8d179ae30d",
            MCP_GITHUB_TOKEN: "ghp_YOUR_TOKEN_PLACEHOLDER"
        };

        const envPath = path.join(this.projectRoot, '.env');
        const envContent = Object.entries(envConfig)
            .map(([key, value]) => `${key}=${value}`)
            .join('\n');
        fs.writeFileSync(envPath, envContent);
        console.log(`创建环境变量配置: ${envPath}`);
    }

    /**
     * 部署技能文件
     */
    async deploySkills() {
        console.log('📚 部署技能文件...');

        const skillsDir = path.join(this.projectRoot, 'skills');
        if (!fs.existsSync(skillsDir)) {
            fs.mkdirSync(skillsDir, { recursive: true });
        }

        // 创建技能索引文件
        const skillIndex = {
            version: '2.0.0',
            totalSkills: 78,
            categories: [],
            lastUpdated: new Date().toISOString(),
            skills: []
        };

        // 扫描并复制技能
        for (const skillDir of this.existingSkillDirs) {
            await this.copySkillsFromDir(skillDir, skillsDir, skillIndex);
        }

        // 保存技能索引
        const indexPath = path.join(skillsDir, 'index.json');
        fs.writeFileSync(indexPath, JSON.stringify(skillIndex, null, 2));
        console.log(`创建技能索引: ${indexPath}`);
    }

    /**
     * 从目录复制技能
     */
    async copySkillsFromDir(sourceDir, destDir, skillIndex) {
        const entries = fs.readdirSync(sourceDir, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(sourceDir, entry.name);
            const destPath = path.join(destDir, entry.name);

            if (entry.isDirectory()) {
                // 检查是否为技能目录
                const skillMdPath = path.join(fullPath, 'SKILL.md');
                if (fs.existsSync(skillMdPath)) {
                    // 复制技能目录
                    fs.cpSync(fullPath, destPath, { recursive: true });

                    // 解析技能信息
                    const skillContent = fs.readFileSync(skillMdPath, 'utf8');
                    const skill = this.parseSkillMetadata(skillContent);

                    skillIndex.skills.push({
                        name: skill.name,
                        category: skill.category || '未分类',
                        path: destPath,
                        version: skill.version || '1.0.0',
                        triggers: skill.triggers || []
                    });

                    if (!skillIndex.categories.includes(skill.category)) {
                        skillIndex.categories.push(skill.category || '未分类');
                    }

                    console.log(`复制技能: ${skill.name} (${skill.category})`);
                }
            }
        }
    }

    /**
     * 解析技能元数据
     */
    parseSkillMetadata(content) {
        const skill = {};
        const lines = content.split('\n');

        lines.forEach(line => {
            if (line.startsWith('name:')) {
                skill.name = line.split(':')[1].trim();
            } else if (line.startsWith('description:')) {
                skill.description = line.split(':')[1].trim();
            } else if (line.startsWith('version:')) {
                skill.version = line.split(':')[1].trim();
            } else if (line.startsWith('category:')) {
                skill.category = line.split(':')[1].trim();
            }
        });

        return skill;
    }

    /**
     * 创建启动脚本
     */
    async createStartupScripts() {
        console.log('📝 创建启动脚本...');

        // 创建Windows启动脚本
        const windowsScript = `@echo off
echo 启动通神认证Agent...
cd /d "%~dp0"
node core-scheduler.js
pause`;
        fs.writeFileSync(path.join(this.projectRoot, 'start.bat'), windowsScript);

        // 创建Linux/Mac启动脚本
        const unixScript = `#!/bin/bash
echo "启动通神认证Agent..."
cd "$(dirname "$0")"
node core-scheduler.js`;
        fs.writeFileSync(path.join(this.projectRoot, 'start.sh'), unixScript);
        fs.chmodSync(path.join(this.projectRoot, 'start.sh'), '755');

        // 创建PM2配置
        const pm2Config = {
            apps: [{
                name: 'tongshen-auth-agent',
                script: 'core-scheduler.js',
                instances: 1,
                exec_mode: 'cluster',
                env: {
                    NODE_ENV: 'production',
                    TONGSHEN_AGENT_ENABLED: 'true'
                },
                error_file: 'logs/agent-error.log',
                out_file: 'logs/agent-out.log',
                log_file: 'logs/agent.log',
                time: true
            }]
        };

        fs.writeFileSync(path.join(this.projectRoot, 'ecosystem.config.js'), JSON.stringify(pm2Config, null, 2));
        console.log('创建PM2配置: ecosystem.config.js');
    }

    /**
     * 测试部署
     */
    async testDeployment() {
        console.log('🧪 测试部署...');

        const TongshenCoreScheduler = require('./core-scheduler');
        const scheduler = new TongshenCoreScheduler();

        return new Promise((resolve) => {
            scheduler.on('initialized', async () => {
                console.log('✅ 调度器初始化成功');

                try {
                    // 测试技能加载
                    const skills = scheduler.getSkills();
                    console.log(`✅ 加载了 ${skills.length} 个技能`);

                    // 测试技能查找
                    const testSkill = scheduler.findSkill('通神');
                    if (testSkill) {
                        console.log('✅ 技能查找功能正常');
                    }

                    // 测试简单任务
                    const result = await scheduler.schedule('测试');
                    console.log('✅ 简单任务执行成功');

                    resolve(true);
                } catch (error) {
                    console.error('❌ 测试失败:', error);
                    resolve(false);
                }
            });

            // 设置超时
            setTimeout(() => {
                console.log('⚠️ 测试超时');
                resolve(false);
            }, 30000);
        });
    }

    /**
     * 回滚部署
     */
    async rollback() {
        console.log('🔄 回滚部署...');

        if (fs.existsSync(this.backupDir)) {
            const claudeMdPath = path.join(this.projectRoot, 'claude.md');
            const backupFiles = fs.readdirSync(this.backupDir)
                .filter(file => file.includes('.backup'));

            if (backupFiles.length > 0) {
                const latestBackup = backupFiles.sort().pop();
                const backupPath = path.join(this.backupDir, latestBackup);

                if (fs.existsSync(claudeMdPath)) {
                    fs.unlinkSync(claudeMdPath);
                }
                fs.copyFileSync(backupPath, claudeMdPath);
                console.log(`从 ${latestBackup} 回滚claude.md`);
            }
        }
    }
}

// 如果直接运行，执行部署
if (require.main === module) {
    const deployment = new ClaudeDeployment();

    // 解析命令行参数
    const args = process.argv.slice(2);
    if (args.includes('--no-backup')) {
        deployment.config.backup = false;
    }
    if (args.includes('--no-test')) {
        deployment.config.test = false;
    }
    if (args.includes('--quiet')) {
        deployment.config.verbose = false;
    }

    // 执行部署
    deployment.deploy()
        .then(success => {
            if (success) {
                console.log('\n🎉 部署成功！');
                console.log('\n下一步:');
                console.log('1. 运行 start.sh 或 start.bat 启动服务');
                console.log('2. 访问 http://localhost:3000 查看管理界面');
                console.log('3. 查看日志: logs/tongshen.log');
            } else {
                process.exit(1);
            }
        })
        .catch(error => {
            console.error('部署过程中发生错误:', error);
            process.exit(1);
        });
}

module.exports = ClaudeDeployment;