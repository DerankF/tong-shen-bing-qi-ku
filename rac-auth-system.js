/**
 * RAC认证体系 - 认证、授权、计费
 * Rights Authorization Charging
 */

const EventEmitter = require('events');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

class RACAuthSystem extends EventEmitter {
    constructor() {
        super();
        this.version = 'v2.0.0';
        this.name = 'RAC认证体系';

        // 认证状态
        this.users = new Map(); // 用户信息
        this.tokens = new Map(); // 访问令牌
        this.roles = new Map(); // 角色定义
        this.permissions = new Map(); // 权限定义
        this.subscriptions = new Map(); // 订阅信息
        this.usage = new Map(); // 使用记录

        // 默认配置
        this.config = {
            tokenExpiry: 24 * 60 * 60 * 1000, // 24小时
            refreshTokenExpiry: 7 * 24 * 60 * 60 * 1000, // 7天
            maxFailedAttempts: 5,
            lockoutDuration: 15 * 60 * 1000, // 15分钟
            rateLimit: {
                requests: 100,
                window: 60 * 60 * 1000 // 1小时
            }
        };

        // 初始化默认角色和权限
        this.initializeDefaultRoles();
        this.loadUserData();
    }

    /**
     * 初始化默认角色
     */
    initializeDefaultRoles() {
        // 超级管理员
        this.roles.set('super_admin', {
            id: 'super_admin',
            name: '超级管理员',
            permissions: [
                'user:create',
                'user:read',
                'user:update',
                'user:delete',
                'role:create',
                'role:read',
                'role:update',
                'role:delete',
                'permission:assign',
                'system:config',
                'skill:execute',
                'skill:manage',
                'api:access',
                'billing:manage'
            ],
            subscription: 'unlimited'
        });

        // 普通用户
        this.roles.set('user', {
            id: 'user',
            name: '普通用户',
            permissions: [
                'user:read',
                'skill:execute',
                'api:access'
            ],
            subscription: 'basic'
        });

        // 付费用户
        this.roles.set('premium', {
            id: 'premium',
            name: '付费用户',
            permissions: [
                'user:read',
                'skill:execute',
                'api:access',
                'api:premium',
                'skill:advanced'
            ],
            subscription: 'premium'
        });

        // 企业用户
        this.roles.set('enterprise', {
            id: 'enterprise',
            name: '企业用户',
            permissions: [
                'user:read',
                'user:create',
                'user:update',
                'skill:execute',
                'api:access',
                'api:premium',
                'api:unlimited',
                'skill:advanced',
                'skill:enterprise',
                'billing:manage'
            ],
            subscription: 'enterprise'
        });
    }

    /**
     * 加载用户数据
     */
    loadUserData() {
        const userDataPath = path.join(__dirname, 'data', 'users.json');
        const subscriptionPath = path.join(__dirname, 'data', 'subscriptions.json');

        if (fs.existsSync(userDataPath)) {
            const userData = JSON.parse(fs.readFileSync(userDataPath, 'utf8'));
            for (const user of userData) {
                this.users.set(user.id, user);
            }
        }

        if (fs.existsSync(subscriptionPath)) {
            const subscriptionData = JSON.parse(fs.readFileSync(subscriptionPath, 'utf8'));
            for (const sub of subscriptionData) {
                this.subscriptions.set(sub.userId, sub);
            }
        }
    }

    /**
     * 保存用户数据
     */
    saveUserData() {
        const userDataPath = path.join(__dirname, 'data');
        if (!fs.existsSync(userDataPath)) {
            fs.mkdirSync(userDataPath, { recursive: true });
        }

        // 保存用户数据
        const usersData = Array.from(this.users.values());
        fs.writeFileSync(path.join(userDataPath, 'users.json'), JSON.stringify(usersData, null, 2));

        // 保存订阅数据
        const subscriptionsData = Array.from(this.subscriptions.values());
        fs.writeFileSync(path.join(userDataPath, 'subscriptions.json'), JSON.stringify(subscriptionsData, null, 2));
    }

    /**
     * 用户注册
     */
    async register(userData) {
        const { username, password, email, role = 'user' } = userData;

        // 验证必填字段
        if (!username || !password || !email) {
            throw new Error('缺少必填字段');
        }

        // 检查用户名是否已存在
        if (this.findUserByUsername(username)) {
            throw new Error('用户名已存在');
        }

        // 检查邮箱是否已存在
        if (this.findUserByEmail(email)) {
            throw new Error('邮箱已存在');
        }

        // 创建用户
        const userId = this.generateUserId();
        const hashedPassword = this.hashPassword(password);

        const user = {
            id: userId,
            username,
            email,
            password: hashedPassword,
            role,
            status: 'active',
            createdAt: new Date().toISOString(),
            lastLogin: null,
            failedAttempts: 0,
            lockedUntil: null
        };

        this.users.set(userId, user);

        // 创建订阅
        const subscription = {
            userId,
            type: role,
            status: 'active',
            startedAt: new Date().toISOString(),
            expiresAt: this.calculateSubscriptionExpiry(role),
            features: this.getRoleFeatures(role)
        };

        this.subscriptions.set(userId, subscription);

        // 记录使用量
        this.usage.set(userId, {
            apiCalls: 0,
            skillExecutions: 0,
            bandwidthUsed: 0,
            lastReset: new Date().toISOString()
        });

        this.saveUserData();

        this.emit('userRegistered', user);
        return { user: this.sanitizeUser(user), token: await this.generateToken(userId) };
    }

    /**
     * 用户登录
     */
    async login(username, password) {
        const user = this.findUserByUsername(username);

        if (!user) {
            throw new Error('用户不存在');
        }

        // 检查账户是否锁定
        if (user.lockedUntil && new Date() < new Date(user.lockedUntil)) {
            throw new Error('账户已锁定，请稍后再试');
        }

        // 验证密码
        const isValid = this.verifyPassword(password, user.password);
        if (!isValid) {
            // 增加失败次数
            user.failedAttempts++;

            if (user.failedAttempts >= this.config.maxFailedAttempts) {
                user.lockedUntil = new Date(Date.now() + this.config.lockoutDuration);
                this.saveUserData();
                throw new Error(`账户已锁定，${Math.ceil(this.config.lockoutDuration / 60000)}分钟后重试`);
            }

            this.saveUserData();
            throw new Error('密码错误');
        }

        // 登录成功
        user.failedAttempts = 0;
        user.lastLogin = new Date().toISOString();
        this.saveUserData();

        const token = await this.generateToken(user.id);
        this.emit('userLoggedIn', user);

        return { user: this.sanitizeUser(user), token };
    }

    /**
     * 生成访问令牌
     */
    async generateToken(userId) {
        const token = crypto.randomBytes(32).toString('hex');
        const refreshToken = crypto.randomBytes(32).toString('hex');

        const tokenData = {
            token,
            refreshToken,
            userId,
            expiresAt: new Date(Date.now() + this.config.tokenExpiry),
            refreshTokenExpiresAt: new Date(Date.now() + this.config.refreshTokenExpiry),
            createdAt: new Date().toISOString()
        };

        this.tokens.set(token, tokenData);

        return {
            accessToken: token,
            refreshToken: refreshToken,
            expiresIn: this.config.tokenExpiry / 1000,
            tokenType: 'Bearer'
        };
    }

    /**
     * 验证访问令牌
     */
    verifyToken(token) {
        const tokenData = this.tokens.get(token);
        if (!tokenData) {
            throw new Error('无效的访问令牌');
        }

        if (new Date() > new Date(tokenData.expiresAt)) {
            this.tokens.delete(token);
            throw new Error('访问令牌已过期');
        }

        return tokenData;
    }

    /**
     * 刷新令牌
     */
    refreshToken(refreshToken) {
        const tokenData = Array.from(this.tokens.values())
            .find(t => t.refreshToken === refreshToken);

        if (!tokenData) {
            throw new Error('无效的刷新令牌');
        }

        if (new Date() > new Date(tokenData.refreshTokenExpiresAt)) {
            throw new Error('刷新令牌已过期');
        }

        // 生成新令牌
        const newToken = await this.generateToken(tokenData.userId);

        // 删除旧令牌
        this.tokens.delete(tokenData.token);

        return newToken;
    }

    /**
     * 执行技能前的权限检查
     */
    async checkSkillPermission(userId, skillName) {
        const user = this.users.get(userId);
        const subscription = this.subscriptions.get(userId);

        if (!user || !subscription) {
            throw new Error('用户不存在');
        }

        if (user.status !== 'active') {
            throw new Error('账户已禁用');
        }

        if (subscription.status !== 'active') {
            throw new Error('订阅已过期');
        }

        // 检查技能权限
        const role = this.roles.get(user.role);
        if (!role) {
            throw new Error('角色不存在');
        }

        // 检查高级技能权限
        if (skillName.includes('volbreak') || skillName.includes('auto-trading')) {
            if (!role.permissions.includes('skill:advanced')) {
                throw new Error('需要高级技能权限');
            }
        }

        // 检查企业级技能权限
        if (skillName.includes('wallstreet') || skillName.includes('enterprise')) {
            if (!role.permissions.includes('skill:enterprise')) {
                throw new Error('需要企业级技能权限');
            }
        }

        // 检查使用量限制
        await this.checkUsageLimits(userId, subscription.type);

        return true;
    }

    /**
     * 检查使用量限制
     */
    async checkUsageLimits(userId, subscriptionType) {
        const usage = this.usage.get(userId);
        if (!usage) {
            return true;
        }

        const limits = this.getSubscriptionLimits(subscriptionType);

        // 检查API调用限制
        if (usage.apiCalls >= limits.apiCalls) {
            throw new Error(`API调用次数已达上限 (${limits.apiCalls}次/月)`);
        }

        // 检查技能执行限制
        if (usage.skillExecutions >= limits.skillExecutions) {
            throw new Error(`技能执行次数已达上限 (${limits.skillExecutions}次/月)`);
        }

        return true;
    }

    /**
     * 记录使用量
     */
    recordUsage(userId, type, amount = 1) {
        const usage = this.usage.get(userId);
        if (usage) {
            if (type === 'api') {
                usage.apiCalls += amount;
            } else if (type === 'skill') {
                usage.skillExecutions += amount;
            }
        }
    }

    /**
     * 更新订阅
     */
    async updateSubscription(userId, newSubscriptionType) {
        const subscription = this.subscriptions.get(userId);
        if (!subscription) {
            throw new Error('订阅不存在');
        }

        subscription.type = newSubscriptionType;
        subscription.updatedAt = new Date().toISOString();
        subscription.expiresAt = this.calculateSubscriptionExpiry(newSubscriptionType);
        subscription.features = this.getRoleFeatures(newSubscriptionType);

        this.saveUserData();
        this.emit('subscriptionUpdated', subscription);

        return subscription;
    }

    /**
     * 获取订阅限制
     */
    getSubscriptionLimits(type) {
        const limits = {
            basic: {
                apiCalls: 100,
                skillExecutions: 50,
                bandwidth: '1GB'
            },
            premium: {
                apiCalls: 1000,
                skillExecutions: 500,
                bandwidth: '10GB'
            },
            enterprise: {
                apiCalls: 10000,
                skillExecutions: 5000,
                bandwidth: '100GB'
            }
        };

        return limits[type] || limits.basic;
    }

    /**
     * 获取角色特性
     */
    getRoleFeatures(role) {
        const roleData = this.roles.get(role);
        return roleData ? roleData.permissions : [];
    }

    /**
     * 计算订阅过期时间
     */
    calculateSubscriptionExpiry(type) {
        const now = new Date();
        if (type === 'enterprise') {
            return new Date(now.setFullYear(now.getFullYear() + 1));
        } else if (type === 'premium') {
            return new Date(now.setMonth(now.getMonth() + 1));
        } else {
            return new Date(now.setMonth(now.getMonth() + 1));
        }
    }

    /**
     * 辅助方法
     */
    generateUserId() {
        return `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    hashPassword(password) {
        return crypto.createHash('sha256').update(password).digest('hex');
    }

    verifyPassword(password, hashedPassword) {
        return this.hashPassword(password) === hashedPassword;
    }

    findUserByUsername(username) {
        return Array.from(this.users.values()).find(u => u.username === username);
    }

    findUserByEmail(email) {
        return Array.from(this.users.values()).find(u => u.email === email);
    }

    sanitizeUser(user) {
        const { password, ...sanitized } = user;
        return sanitized;
    }

    /**
     * 获取用户统计
     */
    getUserStats() {
        const totalUsers = this.users.size;
        const activeUsers = Array.from(this.users.values()).filter(u => u.status === 'active').length;
        const subscriptionStats = {};

        for (const [userId, subscription] of this.subscriptions) {
            subscriptionStats[subscription.type] = (subscriptionStats[subscription.type] || 0) + 1;
        }

        return {
            totalUsers,
            activeUsers,
            subscriptionStats,
            totalTokens: this.tokens.size
        };
    }
}

module.exports = RACAuthSystem;