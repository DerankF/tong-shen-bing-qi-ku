/**
 * 通神认证Agent核心调度器
 * 实现M0元认知、7域路由、链式执行等功能
 */

const EventEmitter = require('events');
const fs = require('fs');
const path = require('path');

class TongshenCoreScheduler extends EventEmitter {
    constructor() {
        super();
        this.version = 'v2.0.0';
        this.name = '通神核心调度器';

        // 核心状态
        this.skills = new Map();
        this.skillCategories = new Map();
        this.triggerMap = new Map();
        this.activeTasks = new Map();
        this.metaCognition = new MetaCognitionModule();
        this.taskChain = new TaskChainManager();
        selfOptimization = true;

        // 性能监控
        this.metrics = {
            totalTasks: 0,
            completedTasks: 0,
            failedTasks: 0,
            avgResponseTime: 0,
            skillUsage: new Map()
        };

        // 初始化
        this.initialize();
    }

    /**
     * 初始化系统
     */
    async initialize() {
        console.log('🚀 启动通神核心调度器');

        // 加载配置
        await this.loadConfiguration();

        // 扫描并加载技能
        await this.scanSkills();

        // 初始化元认知模块
        await this.metaCognition.initialize();

        // 启动自优化循环
        if (this.selfOptimization) {
            this.startOptimizationCycle();
        }

        // 监听技能加载事件
        this.on('skillLoaded', (skill) => {
            console.log(`✅ 技能已加载: ${skill.name} (${skill.category})`);
        });

        this.emit('initialized');
    }

    /**
     * 加载配置
     */
    async loadConfiguration() {
        const configPath = path.join(__dirname, 'SKILL.md');
        if (fs.existsSync(configPath)) {
            const content = fs.readFileSync(configPath, 'utf8');
            this.config = this.parseSkillConfig(content);
        }

        // 加载MCP配置
        const mcpPath = path.join(__dirname, 'mcp-integrated.json');
        if (fs.existsSync(mcpPath)) {
            this.mcpConfig = JSON.parse(fs.readFileSync(mcpPath, 'utf8'));
        }
    }

    /**
     * 扫描技能
     */
    async scanSkills() {
        const scanPaths = [
            'D:\\WorkBuddy',
            'D:\\通神兵器库',
            'D:\\安装位置\\WORKbuddy',
            path.join(__dirname, 'skills')
        ];

        for (const scanPath of scanPaths) {
            if (fs.existsSync(scanPath)) {
                await this.scanDirectory(scanPath);
            }
        }
    }

    /**
     * 扫描目录
     */
    async scanDirectory(dirPath) {
        const entries = fs.readdirSync(dirPath, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);

            if (entry.isDirectory()) {
                // 检查是否为技能目录
                const skillMdPath = path.join(fullPath, 'SKILL.md');
                if (fs.existsSync(skillMdPath)) {
                    await this.loadSkill(fullPath, skillMdPath);
                } else {
                    // 递归扫描子目录
                    await this.scanDirectory(fullPath);
                }
            }
        }
    }

    /**
     * 加载技能
     */
    async loadSkill(skillDir, skillMdPath) {
        try {
            const content = fs.readFileSync(skillMdPath, 'utf8');
            const skill = this.parseSkill(content, skillDir);

            // 按分类存储
            const category = skill.category || '通用';
            if (!this.skillCategories.has(category)) {
                this.skillCategories.set(category, new Map());
            }

            this.skillCategories.get(category).set(skill.name, skill);
            this.skills.set(skill.name, skill);

            // 建立触发词映射
            for (const trigger of skill.triggers) {
                this.triggerMap.set(trigger.toLowerCase(), skill.name);
            }

            // 初始化性能指标
            this.metrics.skillUsage.set(skill.name, {
                count: 0,
                success: 0,
                totalTime: 0,
                avgTime: 0
            });

            this.emit('skillLoaded', skill);
        } catch (error) {
            console.error(`加载技能失败: ${skillDir}`, error);
        }
    }

    /**
     * 解析技能
     */
    parseSkill(content, skillDir) {
        const skill = {
            name: '',
            description: '',
            triggers: [],
            category: '通用',
            path: skillDir,
            version: '1.0.0',
            enabled: true,
            priority: 5,
            dependencies: [],
            config: {}
        };

        const lines = content.split('\n');
        let currentSection = '';

        // 解析YAML头部
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

        // 解析触发词
        const triggerLines = lines.filter(line =>
            line.includes('|') && line.includes('|') && lines.indexOf(line) > 20
        );

        triggerLines.forEach(line => {
            const parts = line.split('|').map(p => p.trim()).filter(p => p);
            if (parts.length >= 3) {
                const triggers = parts[1].split(/[,，\s]+/).filter(t => t);
                skill.triggers.push(...triggers);
            }
        });

        // 如果没有触发词，使用目录名
        if (skill.triggers.length === 0) {
            const dirName = path.basename(skillDir);
            skill.triggers = [dirName.toLowerCase()];
        }

        return skill;
    }

    /**
     * 主要调度方法
     */
    async schedule(request, context = {}) {
        const taskId = this.generateTaskId();
        const startTime = Date.now();

        this.metrics.totalTasks++;
        this.activeTasks.set(taskId, {
            id: taskId,
            request,
            context,
            startTime,
            status: 'running'
        });

        try {
            // 1. 元认知分析
            const metaAnalysis = await this.metaCognition.analyze(request);
            console.log('🧠 元认知分析:', metaAnalysis);

            // 2. 技能路由
            const route = await this.routeSkills(request, metaAnalysis);
            console.log('🎯 技能路由:', route);

            // 3. 执行任务
            const result = await this.executeTask(taskId, route, request, context);

            // 4. 更新性能指标
            const duration = Date.now() - startTime;
            this.updatePerformanceMetrics(route.skills, true, duration);

            // 5. 任务完成
            this.activeTasks.get(taskId).status = 'completed';
            this.activeTasks.get(taskId).result = result;
            this.metrics.completedTasks++;

            this.emit('taskCompleted', {
                taskId,
                request,
                result,
                duration
            });

            return result;

        } catch (error) {
            const duration = Date.now() - startTime;
            this.updatePerformanceMetrics(route?.skills || [], false, duration);

            this.activeTasks.get(taskId).status = 'failed';
            this.activeTasks.get(taskId).error = error;
            this.metrics.failedTasks++;

            this.emit('taskFailed', {
                taskId,
                request,
                error,
                duration
            });

            throw error;
        }
    }

    /**
     * 技能路由
     */
    async routeSkills(request, metaAnalysis) {
        const intent = metaAnalysis.intent;
        const domain = metaAnalysis.domain;

        // 1. 直接触发词匹配
        for (const [trigger, skillName] of this.triggerMap) {
            if (request.toLowerCase().includes(trigger)) {
                const skill = this.skills.get(skillName);
                if (skill && skill.enabled) {
                    return {
                        strategy: 'direct',
                        skills: [skillName],
                        confidence: 0.9,
                        reason: `直接匹配触发词: ${trigger}`
                    };
                }
            }
        }

        // 2. 模糊匹配
        const fuzzyMatches = this.fuzzyMatch(request);
        if (fuzzyMatches.length > 0) {
            return {
                strategy: 'fuzzy',
                skills: fuzzyMatches.map(m => m.skill.name),
                confidence: fuzzyMatches[0].score,
                reason: `模糊匹配得分: ${fuzzyMatches[0].score}`
            };
        }

        // 3. 域路由
        if (domain && this.skillCategories.has(domain)) {
            const domainSkills = Array.from(this.skillCategories.get(domain).values());
            const topSkill = this.selectTopSkill(domainSkills, request);

            return {
                strategy: 'domain',
                skills: [topSkill.name],
                confidence: 0.7,
                reason: `域路由: ${domain}`
            };
        }

        // 4. 通神核心调度
        return {
            strategy: 'meta',
            skills: ['tongshen-v8.1'],
            confidence: 0.5,
            reason: '使用通神元认知调度'
        };
    }

    /**
     * 执行任务
     */
    async executeTask(taskId, route, request, context) {
        const { strategy, skills } = route;

        switch (strategy) {
            case 'direct':
            case 'fuzzy':
                // 单技能执行
                return await this.executeSkill(skills[0], context);

            case 'domain':
                // 域技能执行
                return await this.executeDomainSkill(skills[0], context);

            case 'meta':
                // 通神核心调度
                return await this.metaCognition.execute(request, context);

            case 'chain':
                // 链式执行
                return await this.taskChain.execute(skills, context);

            default:
                throw new Error(`未知路由策略: ${strategy}`);
        }
    }

    /**
     * 执行技能
     */
    async executeSkill(skillName, context) {
        const skill = this.skills.get(skillName);
        if (!skill || !skill.enabled) {
            throw new Error(`技能不可用: ${skillName}`);
        }

        // 检查依赖
        for (const dep of skill.dependencies) {
            if (!this.skills.has(dep)) {
                throw new Error(`依赖技能缺失: ${dep}`);
            }
        }

        // 加载技能实现
        const startTime = Date.now();
        let result;

        try {
            const skillPath = path.join(skill.path, 'index.js');
            if (fs.existsSync(skillPath)) {
                const skillModule = require(skillPath);
                if (typeof skillModule.execute === 'function') {
                    result = await skillModule.execute(context);
                } else {
                    result = { message: `技能 ${skillName} 已执行` };
                }
            } else {
                result = { message: `技能 ${skillName} 已执行` };
            }

            // 记录执行时间
            const duration = Date.now() - startTime;
            this.updateSkillMetrics(skillName, true, duration);

            return result;

        } catch (error) {
            const duration = Date.now() - startTime;
            this.updateSkillMetrics(skillName, false, duration);
            throw error;
        }
    }

    /**
     * 模糊匹配
     */
    fuzzyMatch(query) {
        const matches = [];

        for (const [trigger, skillName] of this.triggerMap) {
            const score = this.calculateSimilarity(query.toLowerCase(), trigger);
            if (score > 0.3) {
                const skill = this.skills.get(skillName);
                matches.push({
                    skill,
                    score,
                    trigger
                });
            }
        }

        return matches.sort((a, b) => b.score - a.score);
    }

    /**
     * 计算相似度
     */
    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;

        if (longer.length === 0) return 1;

        const editDistance = this.levenshteinDistance(longer, shorter);
        return (longer.length - editDistance) / longer.length;
    }

    /**
     * Levenshtein距离
     */
    levenshteinDistance(str1, str2) {
        const matrix = [];

        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }

        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }

        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }

        return matrix[str2.length][str1.length];
    }

    /**
     * 选择顶级技能
     */
    selectTopSkill(skills, query) {
        let topSkill = skills[0];
        let maxScore = 0;

        for (const skill of skills) {
            const score = this.calculateRelevance(skill, query);
            if (score > maxScore) {
                maxScore = score;
                topSkill = skill;
            }
        }

        return topSkill;
    }

    /**
     * 计算相关性
     */
    calculateRelevance(skill, query) {
        const queryLower = query.toLowerCase();
        let score = 0;

        // 描述相关性
        if (skill.description) {
            score += this.calculateSimilarity(queryLower, skill.description.toLowerCase()) * 0.4;
        }

        // 触发词相关性
        for (const trigger of skill.triggers) {
            score += this.calculateSimilarity(queryLower, trigger.toLowerCase()) * 0.3;
        }

        // 分类相关性
        if (skill.category !== '通用') {
            score += 0.2;
        }

        // 优先级
        score += (skill.priority / 10) * 0.1;

        return score;
    }

    /**
     * 更新性能指标
     */
    updatePerformanceMetrics(skillNames, success, duration) {
        skillNames.forEach(name => {
            this.updateSkillMetrics(name, success, duration);
        });

        // 更新平均响应时间
        const totalTasks = this.metrics.totalTasks;
        this.metrics.avgResponseTime =
            (this.metrics.avgResponseTime * (totalTasks - 1) + duration) / totalTasks;
    }

    /**
     * 更新技能指标
     */
    updateSkillMetrics(skillName, success, duration) {
        const metrics = this.metrics.skillUsage.get(skillName);
        if (metrics) {
            metrics.count++;
            if (success) metrics.success++;
            metrics.totalTime += duration;
            metrics.avgTime = metrics.totalTime / metrics.count;
        }
    }

    /**
     * 启动优化循环
     */
    startOptimizationCycle() {
        setInterval(() => {
            this.optimizeSystem();
        }, 60000); // 每分钟优化一次
    }

    /**
     * 系统优化
     */
    async optimizeSystem() {
        console.log('🔧 开始系统优化');

        // 1. 优化技能优先级
        this.optimizeSkillPriorities();

        // 2. 优化触发词
        this.optimizeTriggers();

        // 3. 清理无效技能
        this.cleanupInvalidSkills();

        // 4. 更新路由策略
        this.updateRoutingStrategy();

        console.log('✅ 系统优化完成');
    }

    /**
     * 优化技能优先级
     */
    optimizeSkillPriorities() {
        for (const [name, metrics] of this.metrics.skillUsage) {
            const skill = this.skills.get(name);
            if (skill) {
                // 基于成功率调整优先级
                const successRate = metrics.success / metrics.count;
                if (successRate > 0.8 && skill.priority < 9) {
                    skill.priority++;
                } else if (successRate < 0.5 && skill.priority > 1) {
                    skill.priority--;
                }
            }
        }
    }

    /**
     * 优化触发词
     */
    optimizeTriggers() {
        // 分析用户输入模式
        const triggerAnalysis = this.analyzeTriggerUsage();

        // 添加新的相关触发词
        for (const [trigger, usage] of triggerAnalysis) {
            if (usage.frequency > 10 && usage.successRate > 0.7) {
                // 找到对应的技能
                const skillName = this.triggerMap.get(trigger.toLowerCase());
                if (skillName) {
                    const skill = this.skills.get(skillName);
                    if (skill) {
                        // 添加相关触发词
                        const related = this.findRelatedTriggers(trigger);
                        skill.triggers.push(...related);
                    }
                }
            }
        }

        // 重新建立映射
        this.rebuildTriggerMap();
    }

    /**
     * 分析触发词使用
     */
    analyzeTriggerUsage() {
        // 这里应该从日志中分析
        // 简化实现
        return new Map();
    }

    /**
     * 查找相关触发词
     */
    findRelatedTriggers(trigger) {
        // 简化实现，返回空数组
        return [];
    }

    /**
     * 重建触发词映射
     */
    rebuildTriggerMap() {
        this.triggerMap.clear();

        for (const skill of this.skills.values()) {
            for (const trigger of skill.triggers) {
                this.triggerMap.set(trigger.toLowerCase(), skill.name);
            }
        }
    }

    /**
     * 清理无效技能
     */
    cleanupInvalidSkills() {
        const toRemove = [];

        for (const [name, skill] of this.skills) {
            // 检查技能文件是否存在
            if (!fs.existsSync(skill.path)) {
                toRemove.push(name);
            }

            // 检查长时间未使用的技能
            const metrics = this.metrics.skillUsage.get(name);
            if (metrics && metrics.count === 0) {
                // 保留技能但不清理
            }
        }

        // 删除无效技能
        toRemove.forEach(name => {
            this.skills.delete(name);
            this.metrics.skillUsage.delete(name);
        });
    }

    /**
     * 更新路由策略
     */
    updateRoutingStrategy() {
        // 基于性能数据调整路由策略
        // 简化实现
    }

    /**
     * 生成任务ID
     */
    generateTaskId() {
        return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * 获取统计信息
     */
    getStatistics() {
        return {
            version: this.version,
            totalSkills: this.skills.size,
            skillCategories: Array.from(this.skillCategories.keys()),
            metrics: {
                ...this.metrics,
                uptime: process.uptime()
            },
            activeTasks: this.activeTasks.size,
            lastOptimization: new Date().toISOString()
        };
    }
}

// 元认知模块
class MetaCognitionModule {
    constructor() {
        this.knowledge = new Map();
        this.strategies = new Map();
    }

    async initialize() {
        // 初始化元认知知识
        this.loadKnowledgeBase();
        this.initializeStrategies();
    }

    async analyze(request) {
        // 分析用户意图
        const intent = this.extractIntent(request);

        // 确定领域
        const domain = this.determineDomain(request);

        // 制定策略
        const strategy = this.selectStrategy(intent, domain);

        return {
            intent,
            domain,
            strategy,
            confidence: this.calculateConfidence(request)
        };
    }

    extractIntent(request) {
        // 简化的意图提取
        const lowerRequest = request.toLowerCase();

        if (lowerRequest.includes('分析') || lowerRequest.includes('研究')) {
            return 'analysis';
        } else if (lowerRequest.includes('创建') || lowerRequest.includes('生成')) {
            return 'creation';
        } else if (lowerRequest.includes('部署') || lowerRequest.includes('发布')) {
            return 'deployment';
        } else {
            return 'general';
        }
    }

    determineDomain(request) {
        // 确定领域
        const lowerRequest = request.toLowerCase();

        const domainMap = {
            '交易': '交易/量化',
            '公众号': '内容/公众号',
            '研究': '研究/数据',
            '开发': '开发/部署',
            '部署': '开发/部署'
        };

        for (const [keyword, domain] of Object.entries(domainMap)) {
            if (lowerRequest.includes(keyword)) {
                return domain;
            }
        }

        return '通用';
    }

    selectStrategy(intent, domain) {
        // 选择策略
        if (intent === 'analysis' && domain === '交易/量化') {
            return 'direct';
        } else if (intent === 'creation' && domain === '内容/公众号') {
            return 'chain';
        } else {
            return 'meta';
        }
    }

    calculateConfidence(request) {
        // 计算置信度
        const lowerRequest = request.toLowerCase();
        let confidence = 0.5;

        // 基于关键词增加置信度
        if (lowerRequest.includes('黄金') || lowerRequest.includes('xauusd')) {
            confidence += 0.3;
        }
        if (lowerRequest.includes('公众号')) {
            confidence += 0.3;
        }
        if (lowerRequest.includes('深度')) {
            confidence += 0.2;
        }

        return Math.min(confidence, 1.0);
    }

    async execute(request, context) {
        // 执行元认知调度
        console.log('🧠 执行通神元认知调度');

        // 分解任务
        const tasks = this.decomposeTasks(request);

        // 执行任务链
        const results = [];
        for (const task of tasks) {
            const result = await this.executeTask(task, context);
            results.push(result);
        }

        return {
            strategy: 'meta',
            tasks: tasks,
            results: results,
            summary: this.generateSummary(results)
        };
    }

    decomposeTasks(request) {
        // 简化的任务分解
        return [{
            skill: 'tongshen-v8.1',
            action: 'dispatch',
            request: request
        }];
    }

    async executeTask(task, context) {
        // 执行单个任务
        const scheduler = require('./core-scheduler');
        return await scheduler.executeSkill(task.skill, context);
    }

    generateSummary(results) {
        // 生成摘要
        return {
            totalTasks: results.length,
            successful: results.filter(r => !r.error).length,
            failed: results.filter(r => r.error).length
        };
    }

    loadKnowledgeBase() {
        // 加载知识库
        // 简化实现
    }

    initializeStrategies() {
        // 初始化策略
        this.strategies.set('direct', this.directStrategy);
        this.strategies.set('fuzzy', this.fuzzyStrategy);
        this.strategies.set('chain', this.chainStrategy);
        this.strategies.set('meta', this.metaStrategy);
    }
}

// 任务链管理器
class TaskChainManager {
    constructor() {
        this.chains = new Map();
        this.currentChain = null;
    }

    async execute(skills, context) {
        console.log('🔗 执行任务链');

        const results = [];
        const chainId = this.generateChainId();

        for (const skillName of skills) {
            try {
                const result = await this.executeSkillInChain(skillName, context, chainId);
                results.push({
                    skill: skillName,
                    result: result,
                    success: true
                });

                // 更新上下文
                context = { ...context, ...result };
            } catch (error) {
                results.push({
                    skill: skillName,
                    error: error.message,
                    success: false
                });
            }
        }

        return {
            strategy: 'chain',
            chainId,
            results: results,
            context: context
        };
    }

    async executeSkillInChain(skillName, context, chainId) {
        const scheduler = require('./core-scheduler');
        return await scheduler.executeSkill(skillName, context);
    }

    generateChainId() {
        return `chain_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
}

// 导出模块
module.exports = TongshenCoreScheduler;

// 如果直接运行，启动调度器
if (require.main === module) {
    const scheduler = new TongshenCoreScheduler();

    // 监听事件
    scheduler.on('initialized', () => {
        console.log('✅ 通神核心调度器初始化完成');

        // 示例任务
        scheduler.schedule('分析一下黄金XAUUSD')
            .then(result => {
                console.log('任务结果:', result);
            })
            .catch(error => {
                console.error('任务错误:', error);
            });
    });

    scheduler.on('taskCompleted', (data) => {
        console.log(`✅ 任务完成: ${data.taskId}, 耗时: ${data.duration}ms`);
    });

    scheduler.on('taskFailed', (data) => {
        console.log(`❌ 任务失败: ${data.taskId}, 错误: ${data.error.message}`);
    });
}