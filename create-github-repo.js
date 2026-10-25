#!/usr/bin/env node

/**
 * 创建GitHub仓库并上传项目脚本
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class GitHubRepoCreator {
    constructor() {
        this.repoName = 'tongshen-auth-agent';
        this.repoDescription = '通神认证Agent - 融合78个技能，支持自优化的AI Agent系统';
        this.repoOwner = 'your-username'; // 需要替换为您的GitHub用户名
        this.localPath = process.cwd();
        this.token = 'ghp_YOUR_TOKEN_PLACEHOLDER';
        this.githubApiUrl = 'https://api.github.com';
    }

    /**
     * 执行创建流程
     */
    async create() {
        console.log('🚀 开始创建GitHub仓库并上传项目');
        console.log('='.repeat(50));

        try {
            // 1. 检查环境
            await this.checkEnvironment();

            // 2. 创建本地git仓库
            await this.initializeGitRepo();

            // 3. 创建GitHub仓库
            await this.createGitHubRepo();

            // 4. 添加文件并提交
            await this.addAndCommitFiles();

            // 5. 推送到GitHub
            await this.pushToGitHub();

            console.log('✅ 仓库创建并上传成功！');
            console.log('\n🔗 仓库地址:');
            console.log(`https://github.com/${this.repoOwner}/${this.repoName}`);
            console.log(`https://github.com/${this.repoOwner}/${this.repoName}/tree/main`);

        } catch (error) {
            console.error('❌ 创建失败:', error.message);
            process.exit(1);
        }
    }

    /**
     * 检查环境
     */
    async checkEnvironment() {
        console.log('🔍 检查环境...');

        // 检查git
        try {
            const gitVersion = execSync('git --version', { encoding: 'utf8' });
            console.log(`✅ Git版本: ${gitVersion.trim()}`);
        } catch (error) {
            throw new Error('Git未安装，请先安装Git');
        }

        // 检查Node.js
        const nodeVersion = process.version;
        console.log(`✅ Node.js版本: ${nodeVersion}`);

        // 检查项目文件
        const requiredFiles = [
            'auth-agent-core.js',
            'core-scheduler.js',
            'server.js',
            'deploy-to-claude.js',
            'README.md',
            'SKILL.md'
        ];

        for (const file of requiredFiles) {
            const filePath = path.join(this.localPath, file);
            if (fs.existsSync(filePath)) {
                console.log(`✅ 找到文件: ${file}`);
            } else {
                throw new Error(`缺少必要文件: ${file}`);
            }
        }
    }

    /**
     * 初始化本地git仓库
     */
    async initializeGitRepo() {
        console.log('\n📦 初始化Git仓库...');

        // 检查是否已经是git仓库
        try {
            execSync('git status', { stdio: 'ignore' });
            console.log('✅ 已是Git仓库，跳过初始化');
            return;
        } catch (error) {
            // 不是git仓库，继续初始化
        }

        // 初始化git仓库
        execSync('git init', { cwd: this.localPath });

        // 配置git用户信息
        execSync('git config user.name "通神认证Agent"', { cwd: this.localPath });
        execSync('git config user.email "tongshen@agent.com"', { cwd: this.localPath });

        console.log('✅ Git仓库初始化完成');
    }

    /**
     * 创建GitHub仓库
     */
    async createGitHubRepo() {
        console.log('\n🌐 创建GitHub仓库...');

        const apiUrl = `${this.githubApiUrl}/user/repos`;
        const repoData = {
            name: this.repoName,
            description: this.repoDescription,
            private: false, // 公开仓库
            auto_init: true,
            has_issues: true,
            has_projects: true,
            has_wiki: true,
            has_downloads: true
        };

        const headers = {
            'Authorization': `token ${this.token}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        };

        // 使用curl创建仓库
        const curlCommand = `curl -X POST "${apiUrl}" \
            -H "Authorization: token ${this.token}" \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Content-Type: application/json" \
            -d '${JSON.stringify(repoData)}'`;

        try {
            const response = execSync(curlCommand, { encoding: 'utf8' });
            const repoInfo = JSON.parse(response);

            console.log(`✅ 仓库创建成功: ${repoInfo.full_name}`);
            console.log(`   描述: ${repoInfo.description}`);
            console.log(`   URL: ${repoInfo.html_url}`);
            console.log(`   Clone URL: ${repoInfo.clone_url}`);

        } catch (error) {
            // 如果仓库已存在，跳过创建
            if (error.message.includes('already exists')) {
                console.log('⚠️ 仓库已存在，跳过创建');
            } else {
                throw new Error(`创建GitHub仓库失败: ${error.message}`);
            }
        }
    }

    /**
     * 添加文件并提交
     */
    async addAndCommitFiles() {
        console.log('\n📝 添加文件并提交...');

        // 添加所有文件
        execSync('git add .', { cwd: this.localPath });

        // 提交
        const commitMessage = 'feat: 初始提交 - 通神认证Agent完整项目';
        execSync(`git commit -m "${commitMessage}"`, { cwd: this.localPath });

        console.log('✅ 文件提交完成');
    }

    /**
     * 推送到GitHub
     */
    async pushToGitHub() {
        console.log('\n🚀 推送到GitHub...');

        // 添加远程仓库
        const remoteUrl = `https://github.com/${this.repoOwner}/${this.repoName}.git`;

        try {
            execSync(`git remote add origin ${remoteUrl}`, { cwd: this.localPath });
            console.log('✅ 远程仓库已添加');
        } catch (error) {
            // 远程仓库已存在
            console.log('⚠️ 远程仓库已存在，跳过添加');
        }

        // 推送到GitHub
        execSync('git push -u origin main', {
            cwd: this.localPath,
            stdio: 'inherit'
        });

        console.log('✅ 代码推送完成');
    }
}

// 如果直接运行，执行创建
if (require.main === module) {
    const creator = new GitHubRepoCreator();

    creator.create().catch(error => {
        console.error('创建过程中发生错误:', error);
        process.exit(1);
    });
}

module.exports = GitHubRepoCreator;