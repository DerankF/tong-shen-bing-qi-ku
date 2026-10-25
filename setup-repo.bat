@echo off
chcp 65001 > nul
echo 🚀 开始创建GitHub仓库并上传项目
echo =================================================

:: 设置变量
set repoName=tongshen-auth-agent
set repoDescription=通神认证Agent - 融合78个技能，支持自优化的AI Agent系统
set localPath=%CD%
set token=ghp_YOUR_TOKEN_PLACEHOLDER

:: 检查环境
echo 🔍 检查环境...

:: 检查git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git未安装，请先安装Git
    pause
    exit /b 1
)
echo ✅ Git已安装

:: 检查Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装，请先安装Node.js
    pause
    exit /b 1
)
echo ✅ Node.js已安装

:: 检查必要文件
set requiredFiles=auth-agent-core.js core-scheduler.js server.js deploy-to-claude.js README.md SKILL.md
for %%f in (%requiredFiles%) do (
    if not exist "%%f" (
        echo ❌ 缺少必要文件: %%f
        pause
        exit /b 1
    )
    echo ✅ 找到文件: %%f
)

:: 初始化Git仓库
echo.
echo 📦 初始化Git仓库...

git status >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 已是Git仓库，跳过初始化
) else (
    git init
    git config user.name "通神认证Agent"
    git config user.email "tongshen@agent.com"
    echo ✅ Git仓库初始化完成
)

:: 添加远程仓库
echo.
echo 🌐 添加远程仓库...

git remote -v | findstr "origin" >nul
if %errorlevel% equ 0 (
    echo ⚠️ 远程仓库已存在，跳过添加
) else (
    git remote add origin https://github.com/your-username/%repoName%.git
    echo ✅ 远程仓库已添加
)

:: 添加文件并提交
echo.
echo 📝 添加文件并提交...

git add .
git commit -m "feat: 初始提交 - 通神认证Agent完整项目"
echo ✅ 文件提交完成

:: 推送到GitHub
echo.
echo 🚀 推送到GitHub...

git push -u origin main
if %errorlevel% equ 0 (
    echo ✅ 代码推送完成
) else (
    echo ❌ 推送失败
    echo 可能需要先在GitHub上创建仓库
    echo 请访问 https://github.com/new 创建仓库
    echo 仓库名: %repoName%
    echo 描述: %repoDescription%
    echo 然后重新运行此脚本
    pause
    exit /b 1
)

:: 完成提示
echo.
echo =================================================
echo ✅ 仓库创建并上传成功！
echo 🔗 仓库地址:
echo https://github.com/your-username/%repoName%
echo https://github.com/your-username/%repoName%/tree/main
echo.
echo 📝 下一步:
echo 1. 访问上方链接查看仓库
echo 2. 编辑仓库描述、添加标签等
echo 3. 配置GitHub Pages网站（可选）
echo 4. 设置Actions CI/CD（可选）
echo.
pause