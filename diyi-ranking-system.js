/**
 * 帝意排行榜系统
 * 追踪用户表现、技能使用情况、贡献排名
 */

const EventEmitter = require('events');
const fs = require('fs');
const path = require('path');

class DijiRankingSystem extends EventEmitter {
    constructor() {
        super();
        this.version = 'v2.0.0';
        this.name = '帝意排行榜';

        // 排行榜数据
        this.userRankings = new Map(); // 用户排名
        this.skillStats = new Map(); // 技能统计
        this.dailyRankings = new Map(); // 日排行
        this.weeklyRankings = new Map(); // 周排行
        this.monthlyRankings = new Map(); // 月排行
        this.allTimeRankings = new Map(); // 总排行

        // 帝意积分系统
        this.scoringRules = {
            // 技能执行积分
            'trading-analysis': { base: 100, multiplier: 1.5 },
            'volbreak-backtest': { base: 80, multiplier: 1.3 },
            'volbreak-auto-trading': { base: 200, multiplier: 2.0 },
            'wechat-publisher': { base: 60, multiplier: 1.2 },
            'deep-research': { base: 120, multiplier: 1.8 },
            'deploy-website': { base: 50, multiplier: 1.1 },

            // 通用技能积分
            'basic': { base: 10, multiplier: 1.0 },
            'intermediate': { base: 30, multiplier: 1.5 },
            'advanced': { base: 50, multiplier: 2.0 },
            'expert': { base: 100, multiplier: 3.0 }
        };

        // 排行榜配置
        this.config = {
            updateInterval: 60 * 60 * 1000, // 每小时更新
            historyLimit: 1000, // 历史记录限制
            leaderboardSize: 10, // 排行榜显示数量
            scoringEnabled: true
        };

        this.loadRankingData();
    }

    /**
     * 加载排行榜数据
     */
    loadRankingData() {
        const dataDir = path.join(__dirname, 'data', 'rankings');
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
            return;
        }

        // 加载用户排名
        const userPath = path.join(dataDir, 'user-rankings.json');
        if (fs.existsSync(userPath)) {
            const data = JSON.parse(fs.readFileSync(userPath, 'utf8'));
            for (const [userId, ranking] of Object.entries(data)) {
                this.userRankings.set(userId, ranking);
            }
        }

        // 加载技能统计
        const skillPath = path.join(dataDir, 'skill-stats.json');
        if (fs.existsSync(skillPath)) {
            const data = JSON.parse(fs.readFileSync(skillPath, 'utf8'));
            for (const [skillName, stats] of Object.entries(data)) {
                this.skillStats.set(skillName, stats);
            }
        }

        // 加载时间排行
        this.loadTimeRankings(dataDir);
    }

    /**
     * 加载时间排行榜数据
     */
    loadTimeRankings(dataDir) {
        const periods = ['daily', 'weekly', 'monthly', 'alltime'];

        for (const period of periods) {
            const filePath = path.join(dataDir, `${period}-rankings.json`);
            if (fs.existsSync(filePath)) {
                const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
                this[`${period}Rankings`] = new Map(Object.entries(data));
            }
        }
    }

    /**
     * 保存排行榜数据
     */
    saveRankingData() {
        const dataDir = path.join(__dirname, 'data', 'rankings');
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }

        // 保存用户排名
        const userRankingsData = Object.fromEntries(this.userRankings);
        fs.writeFileSync(path.join(dataDir, 'user-rankings.json'), JSON.stringify(userRankingsData, null, 2));

        // 保存技能统计
        const skillStatsData = Object.fromEntries(this.skillStats);
        fs.writeFileSync(path.join(dataDir, 'skill-stats.json'), JSON.stringify(skillStatsData, null, 2));

        // 保存时间排行
        this.saveTimeRankings(dataDir);
    }

    /**
     * 保存时间排行榜
     */
    saveTimeRankings(dataDir) {
        const periods = ['daily', 'weekly', 'monthly', 'alltime'];

        for (const period of periods) {
            const rankings = this[`${period}Rankings`];
            const filePath = path.join(dataDir, `${period}-rankings.json`);
            const rankingsData = Object.fromEntries(rankings);
            fs.writeFileSync(filePath, JSON.stringify(rankingsData, null, 2));
        }
    }

    /**
     * 记录技能执行
     */
    recordSkillExecution(userId, skillName, skillLevel = 'basic', success = true, executionTime = 0) {
        if (!this.config.scoringEnabled) return;

        // 获取评分规则
        const scoringRule = this.scoringRules[skillName] || this.scoringRules[skillLevel];

        // 计算积分
        let points = scoringRule.base;
        if (success) {
            points *= scoringRule.multiplier;

            // 速度奖励
            if (executionTime < 1000) { // 1秒内完成
                points *= 1.2;
            } else if (executionTime < 5000) { // 5秒内完成
                points *= 1.1;
            }
        } else {
            points *= 0.5; // 失败只获得一半积分
        }

        // 更新用户排名
        this.updateUserRanking(userId, Math.floor(points), skillName);

        // 更新技能统计
        this.updateSkillStats(skillName, userId, success);

        // 更新时间排行
        this.updateTimeRankings(userId, Math.floor(points));

        this.emit('skillRecorded', {
            userId,
            skillName,
            points: Math.floor(points),
            success,
            executionTime
        });
    }

    /**
     * 更新用户排名
     */
    updateUserRanking(userId, points, skillName) {
        let ranking = this.userRankings.get(userId);

        if (!ranking) {
            ranking = {
                userId,
                username: `user_${userId}`,
                totalPoints: 0,
                skillCount: 0,
                successfulExecutions: 0,
                failedExecutions: 0,
                skillMastery: {},
                achievements: [],
                lastActive: new Date().toISOString(),
                createdAt: new Date().toISOString()
            };
            this.userRankings.set(userId, ranking);
        }

        // 更新统计
        ranking.totalPoints += points;
        ranking.skillCount++;
        ranking.lastActive = new Date().toISOString();

        if (points > 0) {
            ranking.successfulExecutions++;
        } else {
            ranking.failedExecutions++;
        }

        // 更新技能掌握度
        const masteryLevel = ranking.skillMastery[skillName] || 0;
        ranking.skillMastery[skillName] = masteryLevel + 1;

        // 检查成就
        this.checkAchievements(ranking, skillName, points);

        // 排序
        this.sortUserRankings();

        this.saveRankingData();
    }

    /**
     * 更新技能统计
     */
    updateSkillStats(skillName, userId, success) {
        let stats = this.skillStats.get(skillName);

        if (!stats) {
            stats = {
                skillName,
                totalExecutions: 0,
                successfulExecutions: 0,
                failedExecutions: 0,
                uniqueUsers: new Set(),
                totalPoints: 0,
                avgExecutionTime: 0,
                executionTimes: []
            };
            this.skillStats.set(skillName, stats);
        }

        // 更新统计
        stats.totalExecutions++;
        if (success) {
            stats.successfulExecutions++;
        } else {
            stats.failedExecutions++;
        }
        stats.uniqueUsers.add(userId);

        // 更新平均执行时间
        const now = Date.now();
        stats.executionTimes.push(now);
        if (stats.executionTimes.length > 100) {
            stats.executionTimes = stats.executionTimes.slice(-100);
        }

        const totalTime = stats.executionTimes.reduce((sum, time, index) => {
            if (index === 0) return 0;
            return sum + (time - stats.executionTimes[index - 1]);
        }, 0);

        stats.avgExecutionTime = stats.executionTimes.length > 1 ?
            totalTime / (stats.executionTimes.length - 1) : 0;

        this.saveRankingData();
    }

    /**
     * 更新时间排行榜
     */
    updateTimeRankings(userId, points) {
        const now = new Date();
        const date = now.toISOString().split('T')[0];

        // 日排行
        this.updatePeriodRanking(this.dailyRankings, userId, points, date);

        // 周排行
        const weekStart = this.getWeekStart(now);
        this.updatePeriodRanking(this.weeklyRankings, userId, points, weekStart);

        // 月排行
        const monthStart = this.getMonthStart(now);
        this.updatePeriodRanking(this.monthlyRankings, userId, points, monthStart);

        // 总排行
        this.updatePeriodRanking(this.allTimeRankings, userId, points, 'alltime');
    }

    /**
     * 更新时间段排行榜
     */
    updatePeriodRanking(rankingMap, userId, points, period) {
        const key = `${period}_${userId}`;
        let ranking = rankingMap.get(key);

        if (!ranking) {
            const user = this.userRankings.get(userId);
            ranking = {
                key,
                userId,
                username: user ? user.username : `user_${userId}`,
                points: 0,
                period,
                lastUpdate: new Date().toISOString()
            };
            rankingMap.set(key, ranking);
        }

        ranking.points += points;
        ranking.lastUpdate = new Date().toISOString();

        // 排序
        this.sortPeriodRankings(rankingMap);
    }

    /**
     * 排序用户排名
     */
    sortUserRankings() {
        const sorted = Array.from(this.userRankings.values())
            .sort((a, b) => b.totalPoints - a.totalPoints)
            .slice(0, this.config.historyLimit);

        this.userRankings.clear();
        for (const ranking of sorted) {
            this.userRankings.set(ranking.userId, ranking);
        }
    }

    /**
     * 排序时间段排名
     */
    sortPeriodRankings(rankingMap) {
        const sorted = Array.from(rankingMap.values())
            .sort((a, b) => b.points - a.points)
            .slice(0, this.config.leaderboardSize);

        rankingMap.clear();
        for (const ranking of sorted) {
            rankingMap.set(ranking.key, ranking);
        }
    }

    /**
     * 检查成就
     */
    checkAchievements(ranking, skillName, points) {
        const achievements = [];

        // 总积分成就
        if (ranking.totalPoints >= 1000 && !ranking.achievements.includes('first_1000')) {
            achievements.push({
                id: 'first_1000',
                name: '初出茅庐',
                description: '累计获得1000积分',
                icon: '🌟',
                points: 1000,
                earnedAt: new Date().toISOString()
            });
        }

        if (ranking.totalPoints >= 10000 && !ranking.achievements.includes('skill_master')) {
            achievements.push({
                id: 'skill_master',
                name: '技能大师',
                description: '累计获得10000积分',
                icon: '🏆',
                points: 10000,
                earnedAt: new Date().toISOString()
            });
        }

        // 技能数量成就
        const skillCount = Object.keys(ranking.skillMastery).length;
        if (skillCount >= 10 && !ranking.achievements.includes('skill_explorer')) {
            achievements.push({
                id: 'skill_explorer',
                name: '技能探索者',
                description: '掌握10种不同技能',
                icon: '🔍',
                points: 500,
                earnedAt: new Date().toISOString()
            });
        }

        // 成功率成就
        const successRate = ranking.successfulExecutions / ranking.skillCount;
        if (successRate >= 0.9 && ranking.skillCount >= 50 && !ranking.achievements.includes('perfectionist')) {
            achievements.push({
                id: 'perfectionist',
                name: '完美主义者',
                description: '成功率90%以上（执行50次）',
                icon: '💯',
                points: 800,
                earnedAt: new Date().toISOString()
            });
        }

        // 特殊技能成就
        if (skillName === 'volbreak-auto-trading' && ranking.skillMastery[skillName] >= 5 && !ranking.achievements.includes('trading_expert')) {
            achievements.push({
                id: 'trading_expert',
                name: '交易专家',
                description: '成功执行5次自动交易',
                icon: '📈',
                points: 1500,
                earnedAt: new Date().toISOString()
            });
        }

        if (skillName === 'deep-research' && ranking.skillMastery[skillName] >= 10 && !ranking.achievements.includes('research_master')) {
            achievements.push({
                id: 'research_master',
                name: '研究大师',
                description: '成功执行10次深度研究',
                icon: '🔬',
                points: 1200,
                earnedAt: new Date().toISOString()
            });
        }

        // 更新成就
        achievements.forEach(achievement => {
            if (!ranking.achievements.find(a => a.id === achievement.id)) {
                ranking.achievements.push(achievement);
            }
        });

        if (achievements.length > 0) {
            this.emit('achievementUnlocked', {
                userId: ranking.userId,
                achievements
            });
        }
    }

    /**
     * 获取用户排名
     */
    getUserRanking(userId) {
        const allUsers = Array.from(this.userRankings.values());
        const userRanking = allUsers.findIndex(u => u.userId === userId) + 1;

        return {
            rank: userRanking,
            totalUsers: allUsers.length,
            user: this.userRankings.get(userId)
        };
    }

    /**
     * 获取排行榜
     */
    getLeaderboard(period = 'daily', limit = 10) {
        let rankings = this[`${period}Rankings`];

        if (!rankings) {
            rankings = new Map();
        }

        return Array.from(rankings.values())
            .slice(0, limit)
            .map((ranking, index) => ({
                rank: index + 1,
                ...ranking
            }));
    }

    /**
     * 获取技能统计
     */
    getSkillStats(skillName) {
        return this.skillStats.get(skillName);
    }

    /**
     * 获取热门技能
     */
    getPopularSkills(limit = 10) {
        return Array.from(this.skillStats.values())
            .sort((a, b) => b.totalExecutions - a.totalExecutions)
            .slice(0, limit)
            .map(stats => ({
                skillName: stats.skillName,
                totalExecutions: stats.totalExecutions,
                successRate: stats.totalExecutions > 0 ?
                    (stats.successfulExecutions / stats.totalExecutions * 100).toFixed(1) : 0,
                uniqueUsers: stats.uniqueUsers.size,
                avgExecutionTime: Math.round(stats.avgExecutionTime / 1000 * 10) / 10 // 转换为秒
            }));
    }

    /**
     * 获取成就统计
     */
    getAchievementStats() {
        const allAchievements = new Map();

        for (const ranking of this.userRankings.values()) {
            for (const achievement of ranking.achievements) {
                const count = allAchievements.get(achievement.id) || 0;
                allAchievements.set(achievement.id, count + 1);
            }
        }

        return Array.from(allAchievements.entries())
            .map(([id, count]) => {
                const achievement = this.getAchievementDefinition(id);
                return {
                    ...achievement,
                    count
                };
            })
            .sort((a, b) => b.count - a.count);
    }

    /**
     * 获取成就定义
     */
    getAchievementDefinition(id) {
        const definitions = {
            'first_1000': {
                id: 'first_1000',
                name: '初出茅庐',
                description: '累计获得1000积分',
                icon: '🌟',
                rarity: 'common'
            },
            'skill_master': {
                id: 'skill_master',
                name: '技能大师',
                description: '累计获得10000积分',
                icon: '🏆',
                rarity: 'rare'
            },
            'skill_explorer': {
                id: 'skill_explorer',
                name: '技能探索者',
                description: '掌握10种不同技能',
                icon: '🔍',
                rarity: 'uncommon'
            },
            'perfectionist': {
                id: 'perfectionist',
                name: '完美主义者',
                description: '成功率90%以上（执行50次）',
                icon: '💯',
                rarity: 'rare'
            },
            'trading_expert': {
                id: 'trading_expert',
                name: '交易专家',
                description: '成功执行5次自动交易',
                icon: '📈',
                rarity: 'epic'
            },
            'research_master': {
                id: 'research_master',
                name: '研究大师',
                description: '成功执行10次深度研究',
                icon: '🔬',
                rarity: 'epic'
            }
        };

        return definitions[id];
    }

    /**
     * 辅助方法
     */
    getWeekStart(date) {
        const d = new Date(date);
        const day = d.getDay();
        const diff = d.getDate() - day;
        return new Date(d.setDate(diff)).toISOString().split('T')[0];
    }

    getMonthStart(date) {
        const d = new Date(date);
        return new Date(d.getFullYear(), d.getMonth(), 1).toISOString().split('T')[0];
    }

    /**
     * 定期更新排行榜
     */
    startPeriodicUpdate() {
        setInterval(() => {
            this.cleanupOldData();
            this.saveRankingData();
        }, this.config.updateInterval);
    }

    /**
     * 清理旧数据
     */
    cleanupOldData() {
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - 30); // 保留30天数据

        // 清理日排行
        this.cleanupPeriodRankings(this.dailyRankings, cutoffDate);

        // 保持周排行和月排行的数据量
        if (this.weeklyRankings.size > 100) {
            const sorted = Array.from(this.weeklyRankings.values())
                .sort((a, b) => b.points - a.points)
                .slice(0, 50);
            this.weeklyRankings.clear();
            for (const ranking of sorted) {
                this.weeklyRankings.set(ranking.key, ranking);
            }
        }

        if (this.monthlyRankings.size > 50) {
            const sorted = Array.from(this.monthlyRankings.values())
                .sort((a, b) => b.points - a.points)
                .slice(0, 30);
            this.monthlyRankings.clear();
            for (const ranking of sorted) {
                this.monthlyRankings.set(ranking.key, ranking);
            }
        }
    }

    /**
     * 清理时间段排名
     */
    cleanupPeriodRankings(rankingMap, cutoffDate) {
        const cutoffStr = cutoffDate.toISOString();
        for (const [key, ranking] of rankingMap) {
            if (new Date(ranking.lastUpdate) < cutoffDate) {
                rankingMap.delete(key);
            }
        }
    }
}

module.exports = DijiRankingSystem;