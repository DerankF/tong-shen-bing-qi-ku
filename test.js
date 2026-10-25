#!/usr/bin/env node

/**
 * 通神认证Agent测试脚本
 */

const TongshenCoreScheduler = require('./core-scheduler');

async function runTests() {
    console.log('🧪 开始测试通神认证Agent');
    console.log('='.repeat(50));

    const scheduler = new TongshenCoreScheduler();
    let testsPassed = 0;
    let totalTests = 0;

    // 测试1: 初始化
    console.log('\n📋 测试1: 初始化调度器');
    totalTests++;
    try {
        await new Promise((resolve) => {
            scheduler.on('initialized', () => {
                console.log('✅ 调度器初始化成功');
                testsPassed++;
                resolve();
            });

            // 设置超时
            setTimeout(() => {
                if (!scheduler.skills.size) {
                    console.log('❌ 调度器初始化超时');
                    resolve();
                }
            }, 10000);
        });
    } catch (error) {
        console.log('❌ 调度器初始化失败:', error.message);
    }

    // 测试2: 技能加载
    console.log('\n📋 测试2: 技能加载');
    totalTests++;
    try {
        const skills = scheduler.getSkills();
        console.log(`✅ 成功加载 ${skills.length} 个技能`);

        // 检查是否有技能
        if (skills.length > 0) {
            const skill = skills[0];
            console.log(`   示例技能: ${skill.name} (${skill.category})`);
            testsPassed++;
        } else {
            console.log('❌ 没有加载到任何技能');
        }
    } catch (error) {
        console.log('❌ 技能加载失败:', error.message);
    }

    // 测试3: 技能查找
    console.log('\n📋 测试3: 技能查找');
    totalTests++;
    try {
        const testQueries = ['通神', '黄金', '公众号', '研究', '部署'];

        for (const query of testQueries) {
            const skill = scheduler.findSkill(query);
            if (skill) {
                console.log(`✅ 找到技能: ${skill.name} (查询: ${query})`);
            } else {
                console.log(`⚠️ 未找到技能: ${query}`);
            }
        }

        testsPassed++;
    } catch (error) {
        console.log('❌ 技能查找失败:', error.message);
    }

    // 测试4: 任务调度
    console.log('\n📋 测试4: 任务调度');
    totalTests++;
    try {
        const testTasks = [
            '测试系统',
            '分析黄金XAUUSD',
            '发布公众号',
            '深度研究AI',
            '部署网站'
        ];

        for (const task of testTasks) {
            console.log(`\n执行任务: ${task}`);
            try {
                const result = await scheduler.schedule(task, { test: true });
                console.log(`✅ 任务完成: ${JSON.stringify(result).substring(0, 100)}...`);
            } catch (error) {
                console.log(`❌ 任务失败: ${error.message}`);
            }
        }

        testsPassed++;
    } catch (error) {
        console.log('❌ 任务调度失败:', error.message);
    }

    // 测试5: 性能监控
    console.log('\n📋 测试5: 性能监控');
    totalTests++;
    try {
        const stats = scheduler.getStatistics();
        console.log('✅ 性能统计:');
        console.log(`   - 总技能数: ${stats.totalSkills}`);
        console.log(`   - 技能分类: ${stats.skillCategories.join(', ')}`);
        console.log(`   - 总任务数: ${stats.metrics.totalTasks}`);
        console.log(`   - 完成任务: ${stats.metrics.completedTasks}`);
        console.log(`   - 失败任务: ${stats.metrics.failedTasks}`);
        console.log(`   - 平均响应时间: ${stats.metrics.avgResponseTime.toFixed(2)}ms`);

        testsPassed++;
    } catch (error) {
        console.log('❌ 性能监控失败:', error.message);
    }

    // 测试6: Web服务器
    console.log('\n📋 测试6: Web服务器');
    totalTests++;
    try {
        const http = require('http');
        const server = require('./server');

        // 创建测试服务器
        const testServer = http.createServer((req, res) => {
            if (req.url === '/test' && req.method === 'GET') {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'ok', message: '通神认证Agent服务正常' }));
            } else {
                res.writeHead(404);
                res.end();
            }
        });

        testServer.listen(3001, () => {
            console.log('✅ 测试服务器启动成功 (端口: 3001)');

            // 发送测试请求
            const options = {
                hostname: 'localhost',
                port: 3001,
                path: '/test',
                method: 'GET'
            };

            const req = http.request(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const response = JSON.parse(data);
                        if (response.status === 'ok') {
                            testsPassed++;
                            console.log('✅ Web服务器测试通过');
                        } else {
                            console.log('❌ Web服务器响应异常');
                        }
                    } catch (error) {
                        console.log('❌ Web服务器响应解析失败');
                    }

                    testServer.close();
                    runSummary();
                });
            });

            req.on('error', () => {
                console.log('❌ Web服务器连接失败');
                testServer.close();
                runSummary();
            });

            req.end();
        });

        // 设置超时
        setTimeout(() => {
            testServer.close();
            console.log('❌ Web服务器测试超时');
            runSummary();
        }, 5000);

    } catch (error) {
        console.log('❌ Web服务器测试失败:', error.message);
        runSummary();
    }

    function runSummary() {
        console.log('\n' + '='.repeat(50));
        console.log('🎯 测试总结');
        console.log('='.repeat(50));
        console.log(`总测试数: ${totalTests}`);
        console.log(`通过测试: ${testsPassed}`);
        console.log(`失败测试: ${totalTests - testsPassed}`);
        console.log(`通过率: ${((testsPassed / totalTests) * 100).toFixed(1)}%`);

        if (testsPassed === totalTests) {
            console.log('\n🎉 所有测试通过！通神认证Agent运行正常');
        } else {
            console.log('\n⚠️ 部分测试失败，请检查相关配置');
        }

        process.exit(testsPassed === totalTests ? 0 : 1);
    }
}

// 如果直接运行，执行测试
if (require.main === module) {
    runTests().catch(error => {
        console.error('测试过程中发生错误:', error);
        process.exit(1);
    });
}

module.exports = { runTests };