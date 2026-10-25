/**
 * 通神认证Agent Web服务器
 * 提供API接口供外部调用
 */

const http = require('http');
const url = require('url');
const querystring = require('querystring');
const { TongshenAuthAgent } = require('./auth-agent-core');

// 初始化认证agent
const agent = new TongshenAuthAgent();

// 创建HTTP服务器
const server = http.createServer((req, res) => {
    // 设置CORS头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    // 处理OPTIONS请求
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    // 解析URL和查询参数
    const parsedUrl = url.parse(req.url);
    const path = parsedUrl.pathname;
    const query = querystring.parse(parsedUrl.query);

    // 设置响应头
    res.setHeader('Content-Type', 'application/json');

    // 根据路径处理请求
    try {
        if (path === '/' || path === '/status') {
            // 状态页面
            handleStatus(res);
        } else if (path === '/skills') {
            // 获取技能列表
            handleSkills(res, query);
        } else if (path === '/skills/find') {
            // 查找技能
            handleFindSkill(res, query);
        } else if (path === '/execute') {
            // 执行技能
            handleExecute(req, res);
        } else if (path === '/stats') {
            // 获取统计信息
            handleStats(res);
        } else if (path === '/export') {
            // 导出配置
            handleExport(res);
        } else if (path === '/import') {
            // 导入配置
            handleImport(req, res);
        } else if (path === '/optimize') {
            // 手动触发优化
            handleOptimize(res);
        } else {
            // 404
            res.writeHead(404);
            res.end(JSON.stringify({ error: 'API endpoint not found' }));
        }
    } catch (error) {
        console.error('请求处理错误:', error);
        res.writeHead(500);
        res.end(JSON.stringify({ error: error.message }));
    }
});

// 处理状态请求
function handleStatus(res) {
    const status = {
        name: agent.name,
        version: agent.version,
        status: 'running',
        uptime: process.uptime(),
        totalSkills: agent.skills.size,
        skillsLoaded: agent.skills.size,
        lastUpdate: new Date().toISOString()
    };

    res.writeHead(200);
    res.end(JSON.stringify(status, null, 2));
}

// 处理技能列表请求
function handleSkills(res, query) {
    let skills = agent.getSkills();

    // 按分类过滤
    if (query.category) {
        skills = skills.filter(skill => skill.category === query.category);
    }

    // 分页
    const page = parseInt(query.page) || 1;
    const limit = parseInt(query.limit) || 20;
    const startIndex = (page - 1) * limit;
    const paginatedSkills = skills.slice(startIndex, startIndex + limit);

    // 返回结果
    const result = {
        skills: paginatedSkills,
        total: skills.length,
        page: page,
        limit: limit,
        categories: Array.from(agent.skillCategories.keys())
    };

    res.writeHead(200);
    res.end(JSON.stringify(result, null, 2));
}

// 处理查找技能请求
function handleFindSkill(res, query) {
    const trigger = query.trigger;

    if (!trigger) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: '缺少trigger参数' }));
        return;
    }

    const skill = agent.findSkill(trigger);

    if (skill) {
        res.writeHead(200);
        res.end(JSON.stringify({
            found: true,
            skill: skill
        }, null, 2));
    } else {
        res.writeHead(200);
        res.end(JSON.stringify({
            found: false,
            message: '未找到匹配的技能'
        }, null, 2));
    }
}

// 处理执行技能请求
async function handleExecute(req, res) {
    let body = '';

    // 读取请求体
    req.on('data', chunk => {
        body += chunk.toString();
    });

    req.on('end', async () => {
        try {
            const data = JSON.parse(body);
            const skillName = data.skill;
            const context = data.context || {};

            if (!skillName) {
                res.writeHead(400);
                res.end(JSON.stringify({ error: '缺少skill参数' }));
                return;
            }

            const result = await agent.executeSkill(skillName, context);

            res.writeHead(200);
            res.end(JSON.stringify({
                success: true,
                result: result
            }, null, 2));
        } catch (error) {
            res.writeHead(400);
            res.end(JSON.stringify({
                success: false,
                error: error.message
            }, null, 2));
        }
    });
}

// 处理统计信息请求
function handleStats(res) {
    const stats = agent.getStatistics();

    res.writeHead(200);
    res.end(JSON.stringify(stats, null, 2));
}

// 处理导出配置请求
function handleExport(res) {
    const config = agent.exportConfiguration();

    res.writeHead(200);
    res.end(JSON.stringify(config, null, 2));
}

// 处理导入配置请求
async function handleImport(req, res) {
    let body = '';

    req.on('data', chunk => {
        body += chunk.toString();
    });

    req.on('end', () => {
        try {
            const config = JSON.parse(body);
            agent.importConfiguration(config);

            res.writeHead(200);
            res.end(JSON.stringify({
                success: true,
                message: '配置导入成功'
            }, null, 2));
        } catch (error) {
            res.writeHead(400);
            res.end(JSON.stringify({
                success: false,
                error: error.message
            }, null, 2));
        }
    });
}

// 处理优化请求
function handleOptimize(res) {
    try {
        agent.optimizeSkills();

        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            message: '优化完成',
            evolutionCycle: agent.evolutionCycle
        }, null, 2));
    } catch (error) {
        res.writeHead(500);
        res.end(JSON.stringify({
            success: false,
            error: error.message
        }, null, 2));
    }
}

// 启动服务器
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`通神认证Agent服务器已启动`);
    console.log(`访问地址: http://localhost:${PORT}`);
    console.log(`API文档: http://localhost:${PORT}/docs`);

    // 显示技能加载情况
    console.log('\n=== 已加载技能分类 ===');
    for (const [category, skills] of agent.skillCategories) {
        console.log(`${category}: ${skills.size}个技能`);
    }

    console.log('\n总技能数量:', agent.skills.size);
    console.log('触发词映射:', agent.triggerMap.size);

    // 监听事件
    agent.on('skillLoaded', (skill) => {
        console.log(`[+] 技能已加载: ${skill.name}`);
    });

    agent.on('skillOptimized', (data) => {
        console.log(`[!] 技能已优化: ${data.skillName}`);
    });

    agent.on('optimizationCycle', (cycle) => {
        console.log(`[🔄] 进化周期 #${cycle}`);
    });
});

// 优雅关闭
process.on('SIGINT', () => {
    console.log('\n正在关闭服务器...');
    server.close(() => {
        console.log('服务器已关闭');
        process.exit(0);
    });
});

// 生成API文档
function generateAPIDoc() {
    const doc = {
        title: '通神认证Agent API',
        version: agent.version,
        endpoints: {
            'GET /': '服务器状态',
            'GET /status': '获取服务器状态',
            'GET /skills': '获取技能列表',
            'GET /skills?category=分类': '按分类获取技能',
            'GET /skills/find?trigger=关键词': '查找技能',
            'POST /execute': '执行技能',
            'GET /stats': '获取统计信息',
            'GET /export': '导出配置',
            'POST /import': '导入配置',
            'POST /optimize': '手动触发优化'
        },
        examples: {
            '查找技能': 'GET /skills/find?trigger=通神',
            '执行技能': 'POST /execute\n{\n  "skill": "trading-analysis",\n  "context": {\n    "symbol": "XAUUSD"\n  }\n}',
            '获取分类列表': 'GET /skills?category=交易/量化'
        }
    };

    fs.writeFileSync(path.join(__dirname, 'api-docs.json'), JSON.stringify(doc, null, 2));
    console.log('API文档已生成: api-docs.json');
}

// 如果提供了--doc参数，生成文档
if (process.argv.includes('--doc')) {
    generateAPIDoc();
}